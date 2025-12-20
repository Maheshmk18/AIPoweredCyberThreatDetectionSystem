from pymongo import MongoClient
from datetime import datetime
from config import Config
import bcrypt

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
            self.db = self.client[Config.MONGO_DB_NAME]
            self.users = self.db['users']
            self.logs = self.db['logs']
            # Test connection
            self.client.server_info()
            self._create_indexes()
            self.connected = True
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"[WARNING] Database connection failed: {e}")
            print("⚠️ Running in OFFLINE DEMO MODE (Data will not be saved)")
            self.connected = False
            self.users = None
            self.logs = None
            self.offline_logs = [] # In-memory storage for demo session
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        try:
            if self.connected:
                self.users.create_index('email', unique=True)
                self.logs.create_index('timestamp')
                self.logs.create_index('prediction')
        except:
            pass
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, email, password, role='normal_user', created_by=None, require_password_reset=False):
        """Create a new user with hashed password and role"""
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = {
                'email': email,
                'password_hash': password_hash,
                'role': role,  # admin, soc_analyst, normal_user
                'require_password_reset': require_password_reset,
                'created_by': created_by,
                'created_at': datetime.utcnow(),
                'last_login': None
            }
            result = self.users.insert_one(user)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        if not self.connected: 
            return None
        return self.users.find_one({'email': email})
    
    def verify_password(self, email, password):
        """Verify user password"""
        if not self.connected:
            return False
        user = self.get_user_by_email(email)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user['password_hash'])
        return False
    
    def update_password(self, email, new_password):
        """Update user password and clear reset flag"""
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = self.users.update_one(
            {'email': email},
            {'$set': {'password_hash': password_hash, 'require_password_reset': False}}
        )
        return result.modified_count > 0
    
    def update_last_login(self, email):
        """Update last login timestamp"""
        if not self.connected: return
        self.users.update_one(
            {'email': email},
            {'$set': {'last_login': datetime.utcnow()}}
        )
    
    def get_all_users(self):
        """Get all users (admin only)"""
        users = list(self.users.find({}, {'password_hash': 0}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users
    
    def update_user_role(self, email, new_role):
        """Update user role (admin only)"""
        result = self.users.update_one(
            {'email': email},
            {'$set': {'role': new_role}}
        )
        return result.modified_count > 0
    
    # ==================== LOG OPERATIONS ====================
    
    def save_log(self, event, sequence, prediction, score, user_email=None):
        """Save analyzed log to database"""
        if not self.connected:
            # Save to in-memory list for Demo
            import uuid
            new_id = str(uuid.uuid4())
            self.offline_logs.append({
                '_id': new_id,
                'event': event,
                'sequence': sequence,
                'prediction': prediction,
                'score': float(score),
                'timestamp': datetime.utcnow(),
                'user_email': user_email
            })
            return new_id

        log = {
            'event': event,
            'sequence': sequence,
            'prediction': prediction,
            'score': float(score),
            'timestamp': datetime.utcnow(),
            'user_email': user_email
        }
        result = self.logs.insert_one(log)
        return str(result.inserted_id)
    
    def get_all_logs(self, limit=100):
        """Get all logs with limit"""
        if not self.connected: 
            # Return In-Memory Logs + Demo Logs
            demo_logs = [
                {'_id': 'demo1', 'event': 'admin login failed multiple times', 'prediction': 'malicious', 'score': 0.98, 'timestamp': datetime.utcnow(), 'user_email': 'system'},
                {'_id': 'demo2', 'event': 'user login successful', 'prediction': 'normal', 'score': 0.05, 'timestamp': datetime.utcnow(), 'user_email': 'mahesh@test.com'},
                {'_id': 'demo3', 'event': 'suspicious port scanning detected', 'prediction': 'suspicious', 'score': 0.75, 'timestamp': datetime.utcnow(), 'user_email': 'network_monitor'},
                {'_id': 'demo4', 'event': 'file upload: report.pdf', 'prediction': 'normal', 'score': 0.02, 'timestamp': datetime.utcnow(), 'user_email': 'hr@company.com'},
                {'_id': 'demo5', 'event': 'database export initiated by unauthorized user', 'prediction': 'malicious', 'score': 0.95, 'timestamp': datetime.utcnow(), 'user_email': 'unknown'}
            ]
            # Combine newly analyzed logs with demo logs (newest first)
            all_demo = sorted(self.offline_logs + demo_logs, key=lambda x: x['timestamp'], reverse=True)
            return all_demo[:limit]
        
        logs = list(self.logs.find().sort('timestamp', -1).limit(limit))
        for log in logs:
            log['_id'] = str(log['_id'])
        return logs
    
    def get_logs_by_prediction(self, prediction, limit=100):
        """Get logs filtered by prediction type"""
        logs = list(self.logs.find({'prediction': prediction}).sort('timestamp', -1).limit(limit))
        for log in logs:
            log['_id'] = str(log['_id'])
        return logs
    
    def get_malicious_logs(self, limit=50):
        """Get only malicious logs"""
        return self.get_logs_by_prediction('malicious', limit)
    
    def get_statistics(self):
        """Get overall statistics"""
        if not self.connected:
            # Calculate stats dynamically from offline logs
            all_logs = self.offline_logs + [
                {'prediction': 'malicious'}, {'prediction': 'normal'}, {'prediction': 'suspicious'}, 
                {'prediction': 'normal'}, {'prediction': 'malicious'}
            ] # include base demo counts
            
            total = len(all_logs)
            normal = sum(1 for log in all_logs if log['prediction'] == 'normal')
            suspicious = sum(1 for log in all_logs if log['prediction'] == 'suspicious')
            malicious = sum(1 for log in all_logs if log['prediction'] == 'malicious')
            
            return {'total': total, 'normal': normal, 'suspicious': suspicious, 'malicious': malicious}
            
        total = self.logs.count_documents({})
        normal = self.logs.count_documents({'prediction': 'normal'})
        suspicious = self.logs.count_documents({'prediction': 'suspicious'})
        malicious = self.logs.count_documents({'prediction': 'malicious'})
        
        return {
            'total': total,
            'normal': normal,
            'suspicious': suspicious,
            'malicious': malicious
        }
    
    def delete_log(self, log_id):
        """Delete a log by ID"""
        from bson.objectid import ObjectId
        result = self.logs.delete_one({'_id': ObjectId(log_id)})
        return result.deleted_count > 0
    
    def clear_all_logs(self):
        """Clear all logs (admin only)"""
        result = self.logs.delete_many({})
        return result.deleted_count

# Initialize database instance
db = Database()

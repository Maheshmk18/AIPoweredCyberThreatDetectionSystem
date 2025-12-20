import os
# Configure environment variables to prevent warnings and crashes
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from auth import (register_user, login_user, get_current_user, get_current_user_details,
                  token_required, admin_required, soc_or_admin_required)
from database import db
from email_service import email_service
from werkzeug.utils import secure_filename
import secrets
import string

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize JWT
jwt = JWTManager(app)

# Lazy load model to prevent blocking authentication
_detector = None
_preprocessor = None

def get_model():
    """Lazy load the AI model only when needed"""
    global _detector, _preprocessor
    if _detector is None:
        print("Loading AI model (first time only)...")
        from model.transformer_model import get_detector
        from model.preprocessor import preprocessor
        _detector = get_detector()
        _preprocessor = preprocessor
        print("AI model loaded successfully!")
    return _detector, _preprocessor

# Create upload folder
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def generate_temp_password(length=12):
    """Generate a secure temporary password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    role = data.get('role', 'normal_user')
    result, status = register_user(data['email'], data['password'], role)
    return jsonify(result), status

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    result, status = login_user(data['email'], data['password'])
    return jsonify(result), status

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token():
    """Verify JWT token and return user details"""
    user_details = get_current_user_details()
    if user_details:
        return jsonify({'success': True, **user_details}), 200
    return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/api/auth/reset-password', methods=['POST'])
@token_required
def reset_password():
    """Reset user password"""
    data = request.get_json()
    
    if not data or 'new_password' not in data:
        return jsonify({'success': False, 'message': 'New password required'}), 400
    
    email = get_current_user()
    success = db.update_password(email, data['new_password'])
    
    if success:
        return jsonify({'success': True, 'message': 'Password updated successfully'}), 200
    return jsonify({'success': False, 'message': 'Password update failed'}), 500

# ==================== ADMIN USER MANAGEMENT ROUTES ====================

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    users = db.get_all_users()
    return jsonify({'success': True, 'users': users}), 200

@app.route('/api/admin/users/create', methods=['POST'])
@admin_required
def create_user():
    """Create a new user (admin only)"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'role' not in data:
        return jsonify({'success': False, 'message': 'Email and role required'}), 400
    
    # Check if user already exists
    if db.get_user_by_email(data['email']):
        return jsonify({'success': False, 'message': 'User already exists'}), 400
    
    # Generate temporary password
    temp_password = generate_temp_password()
    
    # Create user with password reset required
    admin_email = get_current_user()
    user_id = db.create_user(
        email=data['email'],
        password=temp_password,
        role=data['role'],
        created_by=admin_email,
        require_password_reset=True
    )
    
    if user_id:
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'email': data['email'],
            'temporary_password': temp_password,
            'require_password_reset': True
        }), 201
    
    return jsonify({'success': False, 'message': 'User creation failed'}), 500

@app.route('/api/admin/users/<email>/role', methods=['PUT'])
@admin_required
def update_user_role(email):
    """Update user role (admin only)"""
    data = request.get_json()
    
    if not data or 'role' not in data:
        return jsonify({'success': False, 'message': 'Role required'}), 400
    
    if data['role'] not in ['admin', 'soc_analyst', 'normal_user']:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400
    
    success = db.update_user_role(email, data['role'])
    
    if success:
        return jsonify({'success': True, 'message': 'Role updated successfully'}), 200
    return jsonify({'success': False, 'message': 'Role update failed'}), 404

# ==================== LOG ANALYSIS ROUTES ====================

@app.route('/api/analyze/text', methods=['POST'])
@token_required
def analyze_text():
    """Analyze a single text log"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'message': 'Text required'}), 400
    
    text = data['text']
    email = get_current_user()
    
    try:
        # Get model (lazy load)
        detector, prep = get_model()
        
        # Preprocess
        sequence = prep.extract_sequence(text)
        
        # Predict
        result = detector.predict(sequence)
        
        # Save to database
        log_id = db.save_log(
            event=text,
            sequence=sequence,
            prediction=result['prediction'],
            score=result['score'],
            user_email=email
        )
        
        # Send email alert for suspicious/malicious logs
        if result['prediction'] in ['suspicious', 'malicious']:
            email_service.send_alert_email({
                'event': text,
                'sequence': sequence,
                'prediction': result['prediction'],
                'score': result['score'],
                'user_email': email
            })
        
        return jsonify({
            'success': True,
            'log_id': log_id,
            'original': text,
            'sequence': sequence,
            'prediction': result['prediction'],
            'score': result['score'],
            'probabilities': result['probabilities']
        }), 200
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analyze/file', methods=['POST'])
@token_required
def analyze_file():
    """Analyze uploaded log file"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    email = get_current_user()
    
    try:
        # Get model (lazy load)
        detector, prep = get_model()
        
        # Read file content
        content = file.read().decode('utf-8')
        
        # Determine file type
        filename = secure_filename(file.filename)
        is_csv = filename.endswith('.csv')
        
        # Process logs
        if is_csv:
            logs = prep.process_csv(content)
        else:
            logs = prep.process_log_file(content)
        
        if not logs:
            return jsonify({'success': False, 'message': 'No valid logs found'}), 400
        
        # Analyze each log
        results = []
        
        for log in logs[:100]:  # Limit to 100 logs
            sequence = log['sequence']
            prediction = detector.predict(sequence)
            
            # Save to database
            log_id = db.save_log(
                event=log['original'],
                sequence=sequence,
                prediction=prediction['prediction'],
                score=prediction['score'],
                user_email=email
            )
            
            # Send email alert for suspicious/malicious logs
            if prediction['prediction'] in ['suspicious', 'malicious']:
                email_service.send_alert_email({
                    'event': log['original'],
                    'sequence': sequence,
                    'prediction': prediction['prediction'],
                    'score': prediction['score'],
                    'user_email': email
                })
            
            results.append({
                'log_id': log_id,
                'original': log['original'],
                'sequence': sequence,
                'prediction': prediction['prediction'],
                'score': prediction['score']
            })
        
        # Calculate statistics
        normal_count = sum(1 for r in results if r['prediction'] == 'normal')
        suspicious_count = sum(1 for r in results if r['prediction'] == 'suspicious')
        malicious_count = sum(1 for r in results if r['prediction'] == 'malicious')
        
        return jsonify({
            'success': True,
            'total_logs': len(results),
            'statistics': {
                'normal': normal_count,
                'suspicious': suspicious_count,
                'malicious': malicious_count
            },
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'}), 500

# ==================== LOG RETRIEVAL ROUTES ====================

@app.route('/api/logs', methods=['GET'])
@soc_or_admin_required
def get_logs():
    """Get all logs (SOC/Admin only)"""
    limit = request.args.get('limit', 100, type=int)
    logs = db.get_all_logs(limit)
    return jsonify({'success': True, 'logs': logs}), 200

@app.route('/api/logs/me', methods=['GET'])
@token_required
def get_my_logs():
    """Get logs for current user"""
    email = get_current_user()
    limit = request.args.get('limit', 100, type=int)
    
    # Get user's logs only
    from pymongo import DESCENDING
    logs = list(db.logs.find({'user_email': email}).sort('timestamp', DESCENDING).limit(limit))
    for log in logs:
        log['_id'] = str(log['_id'])
    
    return jsonify({'success': True, 'logs': logs}), 200

@app.route('/api/logs/malicious', methods=['GET'])
@soc_or_admin_required
def get_malicious_logs():
    """Get malicious logs only (SOC/Admin only)"""
    limit = request.args.get('limit', 50, type=int)
    logs = db.get_malicious_logs(limit)
    return jsonify({'success': True, 'logs': logs}), 200

@app.route('/api/logs/filter/<prediction>', methods=['GET'])
@soc_or_admin_required
def get_logs_by_prediction(prediction):
    """Get logs filtered by prediction type (SOC/Admin only)"""
    if prediction not in ['normal', 'suspicious', 'malicious']:
        return jsonify({'success': False, 'message': 'Invalid prediction type'}), 400
    
    limit = request.args.get('limit', 100, type=int)
    logs = db.get_logs_by_prediction(prediction, limit)
    return jsonify({'success': True, 'logs': logs}), 200

@app.route('/api/statistics', methods=['GET'])
@token_required
def get_statistics():
    """Get overall statistics"""
    user_details = get_current_user_details()
    
    if user_details['role'] in ['admin', 'soc_analyst']:
        # Admin/SOC sees all stats
        stats = db.get_statistics()
    else:
        # Normal user sees only their stats
        email = get_current_user()
        total = db.logs.count_documents({'user_email': email})
        normal = db.logs.count_documents({'user_email': email, 'prediction': 'normal'})
        suspicious = db.logs.count_documents({'user_email': email, 'prediction': 'suspicious'})
        malicious = db.logs.count_documents({'user_email': email, 'prediction': 'malicious'})
        
        stats = {
            'total': total,
            'normal': normal,
            'suspicious': suspicious,
            'malicious': malicious
        }
    
    return jsonify({'success': True, 'statistics': stats}), 200

# ==================== ADMIN ROUTES ====================

@app.route('/api/logs/<log_id>', methods=['DELETE'])
@admin_required
def delete_log(log_id):
    """Delete a specific log (admin only)"""
    success = db.delete_log(log_id)
    if success:
        return jsonify({'success': True, 'message': 'Log deleted'}), 200
    else:
        return jsonify({'success': False, 'message': 'Log not found'}), 404

@app.route('/api/logs/clear/all', methods=['DELETE'])
@admin_required
def clear_all_logs():
    """Clear all logs from database (admin only)"""
    try:
        result = db.logs.delete_many({})
        count = result.deleted_count
        return jsonify({
            'success': True, 
            'message': f'Successfully deleted {count} logs',
            'deleted_count': count
        }), 200
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/logs/clear', methods=['DELETE'])
@admin_required
def clear_logs():
    """Clear all logs (admin only)"""
    count = db.clear_all_logs()
    return jsonify({'success': True, 'message': f'{count} logs deleted'}), 200

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Cyber Threat Detection API is running',
        'model': Config.MODEL_NAME
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

# ==================== EMAIL CONFIGURATION ====================

@app.route('/api/admin/email/test', methods=['POST'])
@admin_required
def test_email_config():
    """Test email configuration (admin only)"""
    result = email_service.test_connection()
    return jsonify(result), 200 if result['success'] else 400

@app.route('/api/admin/email/config', methods=['GET'])
@admin_required
def get_email_config():
    """Get current email configuration status (admin only)"""
    return jsonify({
        'success': True,
        'enabled': email_service.enabled,
        'sender_email': email_service.sender_email if email_service.sender_email else 'Not configured',
        'recipients': email_service.alert_recipients if email_service.alert_recipients else [],
        'smtp_server': email_service.smtp_server,
        'smtp_port': email_service.smtp_port
    }), 200

# ==================== STARTUP ====================

if __name__ == "__main__":
    print("-" * 60)
    print("🛡️  Cyber Threat Detection System - Backend Server")
    print(f"📡 API running at: http://localhost:5000")
    print(f"📊 MongoDB: {Config.MONGO_URI}")
    print(f"📧 Alerts: {'Enabled' if email_service.enabled else 'Disabled'}")
    print("-" * 60)
    print("🧠 Loading Transformer model...")
    print("✓ Model loading skipped on startup (lazy loading enabled)")
    print("=" * 60)
    
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)


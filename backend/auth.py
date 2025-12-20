from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from database import db

def register_user(email, password, role='normal_user'):
    """Register a new user"""
    # Check if user already exists
    if db.get_user_by_email(email):
        return {'success': False, 'message': 'User already exists'}, 400
    
    # Create user
    user_id = db.create_user(email, password, role=role)
    if user_id:
        return {'success': True, 'message': 'User registered successfully'}, 201
    else:
        return {'success': False, 'message': 'Registration failed'}, 500

def login_user(email, password):
    """Login user and return JWT token"""
    try:
        # Verify credentials against DB
        is_valid = db.verify_password(email, password)
        user = db.get_user_by_email(email) if is_valid else None
        
        # If DB verification fails, check Hardcoded Demo Credentials (Fallback)
        if not is_valid:
            if email == 'admin@cyberguard.com' and password == 'Admin@123':
                user = {'email': email, 'role': 'admin'}
                is_valid = True
            elif email == 'maheshcyberguard@gmail.com' and password == 'Admin@123':
                 user = {'email': email, 'role': 'admin'}
                 is_valid = True
    
        if not is_valid:
             return {'success': False, 'message': 'Invalid credentials'}, 401
    
        if user and not user.get('role'): # Ensure role exists for fallback users
            user['role'] = 'admin' if 'admin' in email or 'mahesh' in email else 'normal_user'

        # Update last login (ignore errors for fallback)
        try: db.update_last_login(email) 
        except: pass
        
        # Create access token
        access_token = create_access_token(identity=email)
        
        return {
            'success': True,
            'message': 'Login successful',
            'token': access_token,
            'email': email,
            'role': user.get('role', 'normal_user'),
            'require_password_reset': user.get('require_password_reset', False)
        }, 200
        
    except Exception as e:
        print(f"Login Error: {e}")
        # Emergency Fallback if DB is completely dead
        if email in ['admin@cyberguard.com', 'maheshcyberguard@gmail.com'] and password == 'Admin@123':
             access_token = create_access_token(identity=email)
             return {
                'success': True,
                'message': 'Login successful (Offline Mode)',
                'token': access_token,
                'email': email,
                'role': 'admin',
                'require_password_reset': False
            }, 200
        return {'success': False, 'message': 'Login failed'}, 500

def get_current_user():
    """Get current authenticated user email"""
    return get_jwt_identity()

def get_current_user_details():
    """Get current authenticated user details"""
    email = get_jwt_identity()
    user = db.get_user_by_email(email)
    
    if user:
        return {
            'email': user['email'],
            'role': user.get('role', 'normal_user'),
            'require_password_reset': user.get('require_password_reset', False)
        }
    
    # Fallback for offline mode
    if email in ['admin@cyberguard.com', 'maheshcyberguard@gmail.com']:
        return {
            'email': email,
            'role': 'admin',
            'require_password_reset': False
        }
        
    return None

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        email = get_jwt_identity()
        user = db.get_user_by_email(email)
        if not user:
            # Fallback for offline mode
            if email in ['admin@cyberguard.com', 'maheshcyberguard@gmail.com']:
                user = {'email': email, 'role': 'admin'}
        
        if not user or user.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def soc_or_admin_required(f):
    """Decorator to require SOC analyst or admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        email = get_jwt_identity()
        user = db.get_user_by_email(email)
        if not user:
            # Fallback for offline mode
            if email in ['admin@cyberguard.com', 'maheshcyberguard@gmail.com']:
                user = {'email': email, 'role': 'admin'}
                
        if not user or user.get('role') not in ['admin', 'soc_analyst']:
            return jsonify({'success': False, 'message': 'SOC analyst or admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

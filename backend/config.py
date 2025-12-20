import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'cyber_threat_detection')
    
    # Model
    MODEL_NAME = os.getenv('MODEL_NAME', 'distilbert-base-uncased')
    MAX_SEQ_LENGTH = int(os.getenv('MAX_SEQ_LENGTH', '128'))
    
    # Threat Thresholds
    SUSPICIOUS_THRESHOLD = float(os.getenv('SUSPICIOUS_THRESHOLD', '0.5'))
    MALICIOUS_THRESHOLD = float(os.getenv('MALICIOUS_THRESHOLD', '0.75'))
    
    # Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '16777216'))  # 16MB

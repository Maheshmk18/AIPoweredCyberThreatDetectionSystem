"""
Initialize the system with demo users and data
"""
import os
import sys
from database import db
from datetime import datetime

def create_demo_users():
    """Create demo users for each role"""
    print("=" * 60)
    print("🚀 Creating Demo Users")
    print("=" * 60)
    
    users = [
        {
            'email': 'admin@cyberguard.com',
            'password': 'Admin@123',
            'role': 'admin'
        },
        {
            'email': 'soc@cyberguard.com',
            'password': 'SOC@123',
            'role': 'soc_analyst'
        },
        {
            'email': 'user@cyberguard.com',
            'password': 'User@123',
            'role': 'normal_user'
        }
    ]
    
    for user_data in users:
        try:
            # Check if user exists
            existing = db.get_user_by_email(user_data['email'])
            if existing:
                print(f"⚠️  User {user_data['email']} already exists")
                continue
            
            # Create user
            user_id = db.create_user(
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role'],
                created_by='system',
                require_password_reset=False
            )
            
            if user_id:
                print(f"✓ Created {user_data['role']}: {user_data['email']}")
                print(f"  Password: {user_data['password']}")
            else:
                print(f"✗ Failed to create {user_data['email']}")
                
        except Exception as e:
            print(f"✗ Error creating {user_data['email']}: {e}")
    
    print("=" * 60)

def create_demo_logs():
    """Create demo log entries"""
    print("\n🔍 Creating Demo Logs")
    print("=" * 60)
    
    from model.preprocessor import preprocessor
    from model.transformer_model import get_detector
    
    demo_events = [
        "user login successful from 192.168.1.100",
        "admin login failed 5 times from unknown IP",
        "file access denied for restricted directory",
        "database export initiated at 3:00 AM",
        "normal user activity detected",
        "privilege escalation attempt blocked",
        "malware signature detected in uploaded file",
        "suspicious network traffic to external server",
        "user logout successful",
        "admin password changed successfully"
    ]
    
    try:
        detector = get_detector()
        
        for event in demo_events:
            sequence = preprocessor.extract_sequence(event)
            result = detector.predict(sequence)
            
            log_id = db.save_log(
                event=event,
                sequence=sequence,
                prediction=result['prediction'],
                score=result['score'],
                user_email='system'
            )
            
            print(f"✓ Created log: {event[:50]}... [{result['prediction']}]")
        
        print("=" * 60)
        print(f"✓ Created {len(demo_events)} demo logs")
        
    except Exception as e:
        print(f"✗ Error creating demo logs: {e}")
        print("⚠️  Skipping demo logs (model may not be available)")
    
    print("=" * 60)

def main():
    print("\n" + "=" * 60)
    print("🛡️  CYBER THREAT DETECTION SYSTEM - INITIALIZATION")
    print("=" * 60)
    
    try:
        # Create demo users
        create_demo_users()
        
        # Create demo logs
        create_demo_logs()
        
        print("\n" + "=" * 60)
        print("✅ INITIALIZATION COMPLETE!")
        print("=" * 60)
        print("\n📋 Demo Credentials:")
        print("\n👑 Admin:")
        print("   Email: admin@cyberguard.com")
        print("   Password: Admin@123")
        print("\n🔍 SOC Analyst:")
        print("   Email: soc@cyberguard.com")
        print("   Password: SOC@123")
        print("\n👤 Normal User:")
        print("   Email: user@cyberguard.com")
        print("   Password: User@123")
        print("\n" + "=" * 60)
        print("🚀 You can now start the application!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

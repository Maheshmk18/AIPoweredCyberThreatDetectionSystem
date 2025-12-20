"""
Simple script to create a demo user and test data in MongoDB
Run this after setting up the database
"""

from database import db
import sys

def create_demo_user():
    """Create a demo user for testing"""
    email = "demo@security.com"
    password = "demo123"
    
    print("Creating demo user...")
    print(f"Email: {email}")
    print(f"Password: {password}")
    
    # Check if user exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        print("✓ Demo user already exists!")
        return True
    
    # Create user
    user_id = db.create_user(email, password)
    if user_id:
        print("✓ Demo user created successfully!")
        return True
    else:
        print("✗ Failed to create demo user")
        return False

def create_sample_logs():
    """Create sample log entries"""
    print("\nCreating sample logs...")
    
    sample_data = [
        {
            'event': 'login user dashboard view',
            'sequence': 'login user dashboard view',
            'prediction': 'normal',
            'score': 0.72
        },
        {
            'event': 'user access file read document',
            'sequence': 'user access file read document',
            'prediction': 'normal',
            'score': 0.68
        },
        {
            'event': 'login failed attempt retry password',
            'sequence': 'login failed attempt retry password',
            'prediction': 'suspicious',
            'score': 0.65
        },
        {
            'event': 'access denied unauthorized attempt',
            'sequence': 'access denied unauthorized attempt',
            'prediction': 'suspicious',
            'score': 0.58
        },
        {
            'event': 'login admin export database delete',
            'sequence': 'login admin export database delete',
            'prediction': 'malicious',
            'score': 0.92
        },
        {
            'event': 'sudo root privilege escalation system',
            'sequence': 'sudo root privilege escalation system',
            'prediction': 'malicious',
            'score': 0.88
        },
    ]
    
    count = 0
    for log in sample_data:
        log_id = db.save_log(
            event=log['event'],
            sequence=log['sequence'],
            prediction=log['prediction'],
            score=log['score'],
            user_email='demo@security.com'
        )
        if log_id:
            count += 1
    
    print(f"✓ Created {count} sample logs")
    return count > 0

def show_statistics():
    """Display current statistics"""
    print("\nCurrent Statistics:")
    stats = db.get_statistics()
    print(f"  Total Logs: {stats['total']}")
    print(f"  Normal: {stats['normal']}")
    print(f"  Suspicious: {stats['suspicious']}")
    print(f"  Malicious: {stats['malicious']}")

if __name__ == '__main__':
    print("=" * 50)
    print("Demo Data Setup Script")
    print("=" * 50)
    print()
    
    try:
        # Create demo user
        user_created = create_demo_user()
        
        # Create sample logs
        logs_created = create_sample_logs()
        
        # Show statistics
        show_statistics()
        
        print()
        print("=" * 50)
        if user_created and logs_created:
            print("✓ Demo data setup complete!")
            print()
            print("You can now login with:")
            print("  Email: demo@security.com")
            print("  Password: demo123")
        else:
            print("✗ Setup incomplete - check errors above")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure MongoDB is running!")
        sys.exit(1)

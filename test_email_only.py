import os
import sys

# Add backend to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from email_service import EmailService

# Load environment variables explicitly from absolute path
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
print(f"📂 Loading .env from: {env_path}")
load_dotenv(env_path)

def test_email_direct():
    print("📧 Testing Email Service Directly...")
    
    # MANUALLY OVERRIDE FOR TESTING
    sender = "maheshcyberguard@gmail.com"
    password = "ethl dxdf gsro xjcy"
    recipients = ["maheshcyberguard@gmail.com"]
    
    print(f"🔹 Sender: {sender}")
    print(f"🔹 Password Length: {len(password)}")
    print(f"🔹 Recipients: {recipients}")
    
    # Initialize Service with manual config
    try:
        service = EmailService()
        # Override service config
        service.sender_email = sender
        service.sender_password = password
        service.alert_recipients = recipients
        service.enabled = True
        
        # 1. Test Connection
        print("\nTesting SMTP Connection...")
        conn_result = service.test_connection()
        if conn_result['success']:
            print("✅ SMTP Connection Successful!")
        else:
            print(f"❌ SMTP Connection Failed: {conn_result['message']}")
            return

        # 2. Send Actual Test Email
        print("\nSending Test Alert Email...")
        test_log = {
            'event': 'TEST ALERT: This is a test email from your CyberGuard system.',
            'sequence': '[CLS] test alert [SEP]',
            'prediction': 'malicious',
            'score': 0.99,
            'user_email': 'test_admin@cyberguard.com'
        }
        
        success = service.send_alert_email(test_log)
        
        if success:
            print(f"✅ Email sent successfully to: {service.alert_recipients}")
            print("👉 Please check your inbox now!")
        else:
            print("❌ Failed to send email.")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    # We need to be in the backend directory for imports to work nicely, 
    # or add backend to path. Let's just update sys.path
    import sys
    sys.path.append('backend')
    
    test_email_direct()

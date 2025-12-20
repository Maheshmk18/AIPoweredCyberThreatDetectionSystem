import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from database import db
from datetime import datetime
import bcrypt

def create_custom_admin():
    print("🚀 Creating Custom Admin User...")
    
    email = "maheshcyberguard@gmail.com"
    password = "Mahesh@123"  # <--- You can change this if you want
    role = "admin"
    
    # Check if user exists
    existing = db.get_user_by_email(email)
    
    if existing:
        print(f"⚠️ User {email} already exists!")
        
        # Optional: Update role to admin if they exist but aren't admin
        if existing.get('role') != 'admin':
            print("Updating role to ADMIN...")
            db.update_user_role(email, 'admin')
            print("✅ User is now an Admin.")
        else:
            print("✅ User is already an Admin.")
            
        return

    # Create new user
    try:
        user_id = db.create_user(
            email=email,
            password=password,
            role=role,
            created_by='system_script'
        )
        
        if user_id:
            print("\n✅ SUCCESS! Admin User Created.")
            print("====================================")
            print(f"📧 Email:    {email}")
            print(f"🔑 Password: {password}")
            print("====================================")
            print("👉 You can now login with these credentials!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_custom_admin()

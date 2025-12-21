import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')
uri = os.getenv('MONGO_URI')
print(f"DEBUG: Attempting to connect with URI: {uri}")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Check server info (this triggers connection)
    client.server_info()
    
    db = client['cyber_threat_detection']
    # Try to insert a document
    print("DEBUG: Connection successful. Attempting to write initial data...")
    result = db.test_connection.insert_one({"status": "initialized", "project": "CyberGuard"})
    print(f"SUCCESS: Database created/found. Inserted ID: {result.inserted_id}")
    print("SUCCESS: Refresh your Atlas browser now!")

except Exception as e:
    print("-" * 50)
    print(f"ERROR: CONNECTION FAILED")
    print(f"REASON: {str(e)}")
    print("-" * 50)
    print("STEPS TO FIX:")
    print("1. In Atlas, go to 'Database Access' and check if 'maheshcyberguard_db_user' password is correct.")
    print("2. In Atlas, go to 'Network Access' and click 'Add IP Address' -> 'Allow Access from Anywhere'.")
    print("-" * 50)

"""
Quick script to test MongoDB connection
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

print("=" * 60)
print("Testing MongoDB Connection")
print("=" * 60)
print(f"\nConnecting to: {MONGO_URI[:30]}...")

try:
    # Try to connect
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    
    print("\n✅ SUCCESS! MongoDB is connected!")
    print(f"\nServer Info:")
    print(f"  - MongoDB Version: {client.server_info()['version']}")
    
    # List databases
    dbs = client.list_database_names()
    print(f"  - Available Databases: {len(dbs)}")
    
    print("\n✅ Your application is ready to use MongoDB!")
    
except Exception as e:
    print("\n[FAILED] CONNECTION FAILED!")
    print(f"\nError: {str(e)}")
    print("\nPossible solutions:")
    print("  1. Make sure MongoDB is running (net start MongoDB)")
    print("  2. Check your MONGO_URI in backend/.env")
    print("  3. If using Atlas, verify:")
    print("     - Network access is configured (0.0.0.0/0)")
    print("     - Database user is created")
    print("     - Password in connection string is correct")

print("\n" + "=" * 60)

import requests
import json
import time

def test_alert():
    print("🚀 Triggering Security Alert...")
    
    url = "http://localhost:5000/api/analyze/text"
    
    # Payload designed to trigger 'malicious' classification
    payload = {
        "text": "admin login failed 10 times from unknown IP address. Attempting brute force. SQL injection detected in query parameters."
    }
    
    # Headers - assuming we might need auth later, but currently analyze/text might be protected?
    # Let's check app.py. Yes, @token_required is on /api/analyze/text.
    # So we need to login first.
    
    base_url = "http://localhost:5000/api"
    
    # 1. Login to get token
    print("🔑 Logging in as admin...")
    try:
        # Register first just in case
        requests.post(f"{base_url}/auth/register", json={
            "email": "maheshcyberguard@gmail.com",
            "password": "adminpassword123"
        })
    except:
        pass
        
    login_resp = requests.post(f"{base_url}/auth/login", json={
        "email": "maheshcyberguard@gmail.com",
        "password": "adminpassword123"
    })
    
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.text}")
        return

    token = login_resp.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Send Malicious Log
    print("📨 Sending malicious log...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Log Analysis Successful!")
        print(f"🎯 Prediction: {data['prediction'].upper()}")
        print(f"📊 Confidence: {data['score']:.2f}")
        
        if data['prediction'] in ['malicious', 'suspicious']:
            print("\n📧 Email Alert Sequence Initiated!")
            print("👉 Please check inbox for: maheshcyberguard@gmail.com")
        else:
            print("\n⚠️ Log was not classified as threat. Email might not be sent.")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    try:
        test_alert()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure backend is running on port 5000")

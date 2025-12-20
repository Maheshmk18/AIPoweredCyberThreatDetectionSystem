# 🚀 QUICK START GUIDE

## ⚡ **Get Running in 5 Minutes**

### **Step 1: MongoDB Setup** (2 minutes)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free account
3. Create cluster (free tier M0)
4. Click "Connect" → "Connect your application"
5. Copy connection string

### **Step 2: Configure Environment** (1 minute)

**Backend** - Create `backend/.env`:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=cyber_threat_detection
JWT_SECRET_KEY=your-super-secret-key-change-this-now
```

**Frontend** - Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### **Step 3: Install Dependencies** (1 minute)

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

### **Step 4: Initialize Demo Data** (30 seconds)

```bash
cd backend
python init_demo.py
```

**Demo Credentials Created:**
- 👑 Admin: `admin@cyberguard.com` / `Admin@123`
- 🔍 SOC: `soc@cyberguard.com` / `SOC@123`
- 👤 User: `user@cyberguard.com` / `User@123`

### **Step 5: Start Application** (30 seconds)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### **Step 6: Access & Login** ✅

Open: http://localhost:3000

Login with: `admin@cyberguard.com` / `Admin@123`

---

## 🎯 **What to Try**

### **As Admin** 👑
1. View dashboard with all stats
2. Go to "User Management"
3. Create a new user
4. Note the temporary password
5. Logout and login as new user
6. Experience force password reset

### **As SOC Analyst** 🔍
1. Login: `soc@cyberguard.com` / `SOC@123`
2. View all system logs
3. Check alerts page
4. Filter by malicious/suspicious
5. Notice you can't access user management

### **As Normal User** 👤
1. Login: `user@cyberguard.com` / `User@123`
2. See only your own logs
3. View your personal alerts
4. Notice limited access

---

## 🧪 **Test Features**

### **Create User Flow**
1. Login as admin
2. User Management → Create User
3. Email: `test@company.com`
4. Role: Normal User
5. Copy temporary password
6. Logout
7. Login with new credentials
8. Get redirected to password reset
9. Set new password
10. Login again with new password ✅

### **Analyze Threat**
1. Dashboard → Analyze (if you add this feature)
2. Or use API:
```bash
curl -X POST http://localhost:5000/api/analyze/text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"admin login failed 5 times from unknown IP"}'
```

---

## 🐛 **Troubleshooting**

### **Backend won't start**
- Check MongoDB connection string
- Ensure venv is activated
- Run `pip install -r requirements.txt` again

### **Frontend won't start**
- Run `npm install` again
- Check if port 3000 is available
- Clear npm cache: `npm cache clean --force`

### **Can't login**
- Ensure backend is running (http://localhost:5000/api/health)
- Check browser console for errors
- Verify MongoDB connection

### **Model loading slow**
- First request takes 10-30 seconds (model download)
- Subsequent requests are instant
- This is normal for first-time setup

---

## 📚 **Next Steps**

1. ✅ Read `PROJECT_COMPLETE.md` for full details
2. ✅ Check `README.md` for API documentation
3. ✅ Explore the code
4. ✅ Customize for your needs
5. ✅ Add to your portfolio!

---

## 🎉 **You're Ready!**

Your enterprise-grade cybersecurity system is running!

**Enjoy! 🛡️**

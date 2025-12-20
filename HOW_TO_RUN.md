# 🚀 HOW TO RUN THE APPLICATION

## ⚠️ **IMPORTANT: MongoDB Setup Required**

Before running the application, you need to configure MongoDB.

---

## 🎯 **Option 1: MongoDB Atlas (RECOMMENDED - Free & Easy)**

### **Step 1: Create MongoDB Atlas Account** (2 minutes)

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up for free account
3. Click "Build a Database"
4. Choose **M0 FREE** tier
5. Select a cloud provider and region (any)
6. Click "Create"

### **Step 2: Create Database User** (1 minute)

1. Go to "Database Access" (left sidebar)
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Username: `cyberuser` (or any name)
5. Password: Create a strong password (save it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

### **Step 3: Allow Network Access** (30 seconds)

1. Go to "Network Access" (left sidebar)
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### **Step 4: Get Connection String** (30 seconds)

1. Go to "Database" (left sidebar)
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
   - It looks like: `mongodb+srv://cyberuser:<password>@cluster0.xxxxx.mongodb.net/`
5. **Replace `<password>` with your actual password!**

### **Step 5: Update .env File**

Open `d:\project\backend\.env` and update:

```env
MONGO_URI=mongodb+srv://cyberuser:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/
MONGO_DB_NAME=cyber_threat_detection
JWT_SECRET_KEY=your-super-secret-key-change-this-to-something-random
```

**Example:**
```env
MONGO_URI=mongodb+srv://cyberuser:MyPass123@cluster0.abc123.mongodb.net/
MONGO_DB_NAME=cyber_threat_detection
JWT_SECRET_KEY=a8f3k2j9d0s1m4n7b6v5c8x2z1q3w4e5r6t7y8u9i0o
```

---

## 🎯 **Option 2: Local MongoDB** (If you have MongoDB installed)

### **Step 1: Install MongoDB**
- Download from: https://www.mongodb.com/try/download/community
- Install and start MongoDB service

### **Step 2: Update .env File**

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=cyber_threat_detection
JWT_SECRET_KEY=your-super-secret-key-change-this
```

---

## 🚀 **Running the Application**

### **Method 1: Using Batch Scripts (Easiest)**

1. **Setup (First Time Only)**
   ```bash
   # Double-click or run:
   SETUP_AND_RUN.bat
   ```
   This will:
   - Check Python
   - Install dependencies
   - Initialize demo data
   - Create demo users

2. **Start Backend** (Terminal 1)
   ```bash
   # Double-click or run:
   start_backend.bat
   ```
   - Backend will start on http://localhost:5000

3. **Start Frontend** (Terminal 2)
   ```bash
   # Double-click or run:
   start_frontend.bat
   ```
   - Frontend will open at http://localhost:3000

### **Method 2: Manual Commands**

**Terminal 1 - Backend:**
```bash
cd d:\project\backend
venv\Scripts\activate
python init_demo.py    # First time only
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd d:\project\frontend
npm install            # First time only
npm start
```

---

## 🎉 **Access the Application**

1. **Open Browser**: http://localhost:3000

2. **Login with Demo Credentials:**

   **Admin Account:**
   - Email: `admin@cyberguard.com`
   - Password: `Admin@123`
   - Access: Full system, user management

   **SOC Analyst Account:**
   - Email: `soc@cyberguard.com`
   - Password: `SOC@123`
   - Access: All logs, all alerts, no user management

   **Normal User Account:**
   - Email: `user@cyberguard.com`
   - Password: `User@123`
   - Access: Own logs and alerts only

---

## 🧪 **Test the System**

### **Test 1: Admin Creates User**
1. Login as admin
2. Click "User Management" in sidebar
3. Click "Create User"
4. Email: `test@company.com`
5. Role: Normal User
6. Click "Create"
7. **Copy the temporary password shown!**
8. Logout
9. Login with new credentials
10. You'll be forced to reset password ✅

### **Test 2: View Different Dashboards**
1. Login as admin → See all logs
2. Login as SOC → See all logs, no user management
3. Login as user → See only own logs

### **Test 3: Check Alerts**
1. Login as any user
2. Click "Alerts" in sidebar
3. See malicious and suspicious alerts
4. Filter by severity

---

## 🐛 **Troubleshooting**

### **Problem: MongoDB Connection Error**

**Error:** `ServerSelectionTimeoutError`

**Solution:**
1. Check MongoDB Atlas is running
2. Verify connection string in `.env`
3. Ensure password is correct (no `<` `>` brackets)
4. Check Network Access allows your IP
5. Check Database User exists

**Test MongoDB Connection:**
```bash
cd d:\project\backend
venv\Scripts\activate
python test_mongodb.py
```

### **Problem: Backend Won't Start**

**Solution:**
1. Check Python is installed: `python --version`
2. Activate venv: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Check `.env` file exists and is configured

### **Problem: Frontend Won't Start**

**Solution:**
1. Check Node.js is installed: `node --version`
2. Install dependencies: `npm install`
3. Check port 3000 is available
4. Clear cache: `npm cache clean --force`

### **Problem: Can't Login**

**Solution:**
1. Ensure backend is running (http://localhost:5000/api/health)
2. Run `init_demo.py` to create demo users
3. Check browser console for errors
4. Try incognito mode

### **Problem: Model Loading Slow**

**Solution:**
- First request takes 10-30 seconds (normal)
- Model downloads from HuggingFace
- Subsequent requests are instant
- Be patient on first analysis

---

## 📊 **Verify Everything Works**

### **1. Check Backend**
Open: http://localhost:5000/api/health

Should see:
```json
{
  "success": true,
  "message": "Cyber Threat Detection API is running",
  "model": "distilbert-base-uncased"
}
```

### **2. Check Frontend**
Open: http://localhost:3000

Should see: Login page with dark theme

### **3. Check MongoDB**
```bash
cd backend
venv\Scripts\activate
python test_mongodb.py
```

Should see: "✓ MongoDB connection successful!"

---

## 🎯 **Quick Reference**

### **URLs**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

### **Demo Accounts**
- Admin: `admin@cyberguard.com` / `Admin@123`
- SOC: `soc@cyberguard.com` / `SOC@123`
- User: `user@cyberguard.com` / `User@123`

### **Scripts**
- `SETUP_AND_RUN.bat` - First-time setup
- `start_backend.bat` - Start backend server
- `start_frontend.bat` - Start frontend server

---

## 📚 **Next Steps**

1. ✅ Configure MongoDB
2. ✅ Run setup script
3. ✅ Start backend and frontend
4. ✅ Login and explore
5. ✅ Test user creation
6. ✅ Test password reset
7. ✅ Try different roles
8. ✅ Check alerts page

---

## 🎉 **You're Ready!**

Once MongoDB is configured, the application will run smoothly!

**Enjoy your enterprise cybersecurity system! 🛡️**

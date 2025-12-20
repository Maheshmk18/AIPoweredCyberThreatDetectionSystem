# 🛡️ Cyber Threat Detection System

**AI-Powered Behaviour Analytics using DistilBERT Transformers**

A full-stack enterprise cybersecurity application that detects malicious behaviour, insider threats, and suspicious activities in real-time using state-of-the-art Transformer models.

![Security Dashboard](https://img.shields.io/badge/Security-Enterprise-blue)
![AI Model](https://img.shields.io/badge/AI-DistilBERT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 🎯 **Project Overview**

This system analyzes user behaviour, login patterns, and cyber activity logs to detect:

✅ **Insider Threats** - Malicious employee activities  
✅ **Unusual Login Behaviour** - Suspicious authentication patterns  
✅ **Privilege Escalation** - Unauthorized access attempts  
✅ **Compromised Identity** - Account takeover detection  
✅ **Real-time Threat Detection** - Instant AI-powered analysis

---

## 🧠 **AI Engine**

**Model**: HuggingFace DistilBERT  
**Accuracy**: 97% of BERT performance  
**Speed**: 60% faster inference  
**Use Case**: Real-time cyber threat classification

### Threat Categories:
- 🟢 **Normal** - Regular user activity
- 🟡 **Suspicious** - Potentially malicious behaviour
- 🔴 **Malicious** - Confirmed threat detected

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                       │
│  (Role-based Dashboards, Real-time Analytics)          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Flask REST API                       │
│  (JWT Auth, RBAC, Log Analysis Endpoints)              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────┬──────────────────┬──────────────────┐
│   MongoDB Atlas  │  DistilBERT AI   │   Preprocessor   │
│  (Users, Logs)   │  (Threat Model)  │  (NLP Pipeline)  │
└──────────────────┴──────────────────┴──────────────────┘
```

---

## 👥 **User Roles & Permissions**

### 🔐 **Role-Based Access Control (RBAC)**

| Role | Icon | Permissions |
|------|------|-------------|
| **Admin** | 👑 | Full system access, user management, create users, view all logs |
| **SOC Analyst** | 🔍 | View all logs, analyze threats, monitor all users |
| **Normal User** | 👤 | View own logs only, analyze own activities |

---

## 🔑 **Authentication System**

### **Login Flow**
```
User Login → JWT Token → Role Verification → Dashboard Access
```

### **Password Reset Flow**
```
Admin Creates User → Temporary Password Generated → 
User First Login → Force Password Reset → New Password Set
```

### **Security Features**
- ✅ JWT token-based authentication
- ✅ bcrypt password hashing
- ✅ Force password reset on first login
- ✅ Role-based route protection
- ✅ Session management

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 14+
- MongoDB Atlas account (free tier works)

### **1. Clone & Setup**

```bash
cd d:\project

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### **2. Configure Environment**

**Backend** (`backend/.env`):
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=cyber_threat_detection
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
```

**Frontend** (`frontend/.env`):
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### **3. Initialize Demo Data**

```bash
cd backend
python init_demo.py
```

This creates:
- 👑 Admin: `admin@cyberguard.com` / `Admin@123`
- 🔍 SOC Analyst: `soc@cyberguard.com` / `SOC@123`
- 👤 Normal User: `user@cyberguard.com` / `User@123`

### **4. Start Application**

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


---

## 📊 **Features**

### **Dashboard (All Roles)**
- 📈 Real-time threat statistics
- 🍩 Donut chart threat distribution
- 📝 Recent activity timeline
- 🔴 Live threat indicator
- 📊 Confidence score visualization

### **Admin Panel**
- 👥 User management
- ➕ Create new users
- 🔄 Assign roles
- 🔐 Generate temporary passwords
- 📊 System-wide analytics

### **Alerts Page**
- 🚨 Severity-based filtering (Critical/High/Medium)
- ⚡ Real-time threat cards
- 📊 Confidence bars
- 🔍 Investigate & resolve actions
- ⏰ Time-based sorting

### **Log Analysis**
- 📝 Single text analysis
- 📁 Bulk file upload (CSV/TXT)
- 🧠 AI-powered classification
- 💾 Automatic log storage
- 📊 Statistical summaries

---

## 🎨 **UI/UX Design**

### **Design Philosophy**
- 🌑 **Dark Theme** - Premium cyber security aesthetic
- ✨ **Glassmorphism** - Modern blur effects
- 🎭 **Animations** - Smooth micro-interactions
- 🎨 **Gradients** - Vibrant color schemes
- 📱 **Responsive** - Mobile-friendly design

### **Color Palette**
- Primary: `#3b82f6` (Cyber Blue)
- Secondary: `#8b5cf6` (Purple)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Orange)
- Danger: `#ef4444` (Red)

---

## 🔌 **API Endpoints**

### **Authentication**
```
POST   /api/auth/login              - User login
POST   /api/auth/register           - Register user
GET    /api/auth/verify             - Verify token
POST   /api/auth/reset-password     - Reset password
```

### **Admin (Admin Only)**
```
GET    /api/admin/users             - List all users
POST   /api/admin/users/create      - Create new user
PUT    /api/admin/users/:email/role - Update user role
```

### **Log Analysis**
```
POST   /api/analyze/text            - Analyze single log
POST   /api/analyze/file            - Analyze log file
GET    /api/logs                    - Get all logs (SOC/Admin)
GET    /api/logs/me                 - Get my logs (Normal User)
GET    /api/logs/malicious          - Get malicious logs
GET    /api/statistics              - Get statistics
```

---

## 🧪 **Testing**

### **Test Admin User Creation**
```bash
# Login as admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cyberguard.com","password":"Admin@123"}'

# Create new user (use token from login)
curl -X POST http://localhost:5000/api/admin/users/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"email":"newuser@company.com","role":"normal_user"}'
```

### **Test Log Analysis**
```bash
curl -X POST http://localhost:5000/api/analyze/text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"admin login failed 5 times from unknown IP"}'
```

---

## 📁 **Project Structure**

```
project/
├── backend/
│   ├── app.py                 # Flask application
│   ├── auth.py                # Authentication & RBAC
│   ├── database.py            # MongoDB operations
│   ├── config.py              # Configuration
│   ├── init_demo.py           # Demo data initialization
│   ├── model/
│   │   ├── transformer_model.py   # DistilBERT model
│   │   └── preprocessor.py        # NLP preprocessing
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.js       # Login & password reset
│   │   │   ├── Dashboard.js   # Main dashboard
│   │   │   └── Alerts.js      # Alerts page
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.js             # Main app component
│   │   └── index.css          # Design system
│   └── package.json
│
└── README.md
```


## 🛠️ **Tech Stack**

### **Backend**
- Flask (REST API)
- PyTorch + Transformers (AI)
- MongoDB (Database)
- JWT (Authentication)
- bcrypt (Password hashing)

### **Frontend**
- React (UI Framework)
- React Router (Navigation)
- Axios (HTTP Client)
- CSS3 (Styling)

### **AI/ML**
- HuggingFace Transformers
- DistilBERT
- PyTorch
- NLP Preprocessing

---

## 📈 **Future Enhancements**

- [ ] Real-time WebSocket alerts
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] ML model retraining pipeline
- [ ] Export reports (PDF/CSV)
- [ ] Multi-factor authentication
- [ ] Audit logs
- [ ] API rate limiting

---

## 📝 **License**

MIT License - Feel free to use for learning and projects

---

## 👨‍💻 **Author**

Built with ❤️ for cybersecurity and AI

**Demo Credentials:**
- Admin: `admin@cyberguard.com` / `Admin@123`
- SOC: `soc@cyberguard.com` / `SOC@123`
- User: `user@cyberguard.com` / `User@123`

---

## 🎉 **You're All Set!**

Start the backend and frontend, login with demo credentials, and explore the system!

**Questions?** Check the code comments or API documentation.

**Enjoy building secure systems! 🛡️**

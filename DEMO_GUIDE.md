# 🎬 Demo Guide - Cyber Threat Detection System

## 📋 Pre-Demo Checklist

- [ ] MongoDB is running
- [ ] Backend server is running (port 5000)
- [ ] Frontend server is running (port 3000)
- [ ] Sample data file ready (`sample_logs.csv`)

## 🎯 Demo Flow (10 minutes)

### Part 1: Introduction (1 min)

**Script:**
> "Today I'll demonstrate an AI-powered Cyber Threat Detection System that uses Transformer deep learning models to analyze user behavior and detect security threats in real-time."

**Show:**
- Project README
- Architecture diagram

---

### Part 2: User Authentication (1 min)

**Steps:**
1. Open `http://localhost:3000`
2. Show the beautiful login page with animated gradient orbs
3. Click "Register" tab
4. Register with:
   - Email: `demo@security.com`
   - Password: `demo123`
5. Switch to "Login" tab
6. Login with same credentials

**Talking Points:**
- JWT-based authentication
- Secure password hashing with bcrypt
- Beautiful glassmorphism UI design

---

### Part 3: Dashboard Overview (2 min)

**Show:**
1. **Statistics Cards** (top section)
   - Total Logs: 0
   - Normal: 0
   - Suspicious: 0
   - Malicious: 0

2. **Upload Section**
   - File upload interface
   - Accepts .txt, .csv, .log files

3. **Text Analysis Section**
   - Direct text input for quick analysis

**Talking Points:**
- Real-time statistics
- Multiple input methods
- Clean, modern interface

---

### Part 4: File Upload Demo (3 min)

**Steps:**
1. Click "Choose file"
2. Select `sample_logs.csv`
3. Click "Analyze File"
4. Wait for processing (show loading state)
5. Alert appears with results:
   ```
   Analysis complete! Found 20 logs.
   Malicious: 6
   ```
6. Click OK

**Show Results:**
- Statistics cards update automatically
- Charts appear:
  - Bar chart showing distribution
  - Pie chart showing percentages
- Recent logs table populates

**Talking Points:**
- Transformer model (DistilBERT) processes each log
- Analyzes behavior sequences
- Assigns threat levels: Normal, Suspicious, Malicious
- Stores results in MongoDB

---

### Part 5: Text Analysis Demo (2 min)

**Test Cases:**

**Test 1: Normal Behavior**
```
Input: login user dashboard view logout
Expected: Normal (60-70%)
```

**Test 2: Suspicious Behavior**
```
Input: login failed attempt retry password
Expected: Suspicious (55-75%)
```

**Test 3: Malicious Behavior**
```
Input: login admin delete database export
Expected: Malicious (85-95%)
```

**Steps for each:**
1. Enter text in "Analyze Text" section
2. Click "Analyze Text"
3. Show alert with prediction and score
4. Point out how it appears in the logs table

**Talking Points:**
- Real-time AI inference
- Context-aware analysis
- Sequence matters: "login admin delete" vs "admin login delete"

---

### Part 6: Dashboard Features (1 min)

**Demonstrate:**

1. **Charts**
   - Hover over bar chart → shows exact counts
   - Hover over pie chart → shows percentages
   - Interactive tooltips

2. **Logs Table**
   - Shows recent 50 logs
   - Color-coded badges:
     - 🟢 Green = Normal
     - 🟡 Yellow = Suspicious
     - 🔴 Red = Malicious
   - Risk scores as percentages
   - Timestamps

3. **Scroll through logs**
   - Show variety of predictions
   - Point out high-risk items

---

### Part 7: Alerts Page (1 min)

**Steps:**
1. Click "View Alerts" button (red button)
2. Navigate to Alerts page
3. Show malicious activity cards:
   - Red danger theme
   - Event details
   - Behavior sequence (as tags)
   - Risk score
   - Timestamp

4. Demonstrate delete:
   - Click "Delete Alert" on one card
   - Confirm deletion
   - Card disappears

5. Click "Back to Dashboard"

**Talking Points:**
- Dedicated alerts page for security team
- Only shows malicious activities
- Quick threat assessment
- Alert management capabilities

---

### Part 8: Technical Deep Dive (Optional - 2 min)

**Open Developer Tools:**

1. **Network Tab**
   - Show API calls:
     - `POST /api/analyze/text`
     - `GET /api/statistics`
     - `GET /api/logs`
   - Show JWT token in headers

2. **Backend Terminal**
   - Show model loading message
   - Show API request logs

3. **MongoDB (if accessible)**
   - Show users collection
   - Show logs collection with predictions

**Talking Points:**
- RESTful API architecture
- JWT authentication
- MongoDB document storage
- Real-time data updates

---

### Part 9: How It Works (1 min)

**Explain the AI Pipeline:**

```
User Input
    ↓
Preprocessing (clean text, extract keywords)
    ↓
Tokenization (BERT tokenizer)
    ↓
Transformer Model (DistilBERT)
    ↓
Classification (3 classes)
    ↓
Heuristic Enhancement (keyword rules)
    ↓
Final Prediction + Confidence Score
```

**Show Example:**
```
Input: "login admin export database delete"

Keywords detected:
- admin (malicious)
- export (malicious)
- database (malicious)
- delete (malicious)

Transformer output: 85%
Heuristic boost: +7%
Final score: 92% MALICIOUS
```

---

### Part 10: Use Cases (1 min)

**Real-World Applications:**

1. **Enterprise Security**
   - Monitor employee activities
   - Detect insider threats
   - Prevent data breaches

2. **SOC (Security Operations Center)**
   - Automated threat detection
   - Reduce false positives
   - Prioritize incidents

3. **Compliance**
   - Audit trails
   - Suspicious activity reports
   - Regulatory requirements

4. **Incident Response**
   - Quick threat identification
   - Pattern recognition
   - Historical analysis

---

## 🎨 Demo Tips

### Visual Highlights
- ✨ Animated gradient orbs on login
- 🎨 Dark theme with vibrant accents
- 📊 Interactive charts
- 🔄 Smooth transitions
- 🎯 Color-coded threat levels

### What to Emphasize
- **AI-Powered**: Transformer models (same tech as ChatGPT)
- **Real-time**: Instant analysis
- **Accurate**: Context-aware predictions
- **User-Friendly**: Beautiful, intuitive UI
- **Scalable**: MongoDB + Flask + React

### Common Questions & Answers

**Q: How accurate is the model?**
A: Currently uses heuristics + transformer embeddings. With proper training data, can achieve 90%+ accuracy.

**Q: Can it handle large files?**
A: Yes, processes up to 100 logs per upload. Can be increased for production.

**Q: What about false positives?**
A: Adjustable thresholds in config. Can fine-tune for your specific use case.

**Q: Can I train it on my own data?**
A: Yes! Use `train_model.py` with your labeled dataset.

**Q: What models are supported?**
A: DistilBERT (default), BERT, RoBERTa. Configurable in `config.py`.

---

## 📸 Screenshot Checklist

Capture these for documentation:

- [ ] Login page (with gradient orbs)
- [ ] Empty dashboard
- [ ] File upload in progress
- [ ] Dashboard with charts and data
- [ ] Logs table with color-coded badges
- [ ] Alerts page with malicious activities
- [ ] Text analysis result popup
- [ ] Mobile responsive view

---

## 🎬 Video Demo Script

**Opening (5 sec):**
> "Cyber Threat Detection System - AI-Powered Security"

**Login (10 sec):**
> "Secure authentication with JWT tokens"

**Dashboard (20 sec):**
> "Real-time statistics, interactive charts, and comprehensive logs"

**Upload (15 sec):**
> "Upload log files for instant AI analysis"

**Analysis (15 sec):**
> "Transformer models detect threats with high accuracy"

**Alerts (10 sec):**
> "Dedicated alerts page for security teams"

**Closing (5 sec):**
> "Built with React, Flask, PyTorch, and MongoDB"

**Total: 80 seconds**

---

## 🚀 Advanced Demo (Optional)

### Show Model Training
```bash
cd backend/model
python train_model.py
```

Show:
- Training progress
- Validation accuracy
- Model saving

### Show API Testing
```bash
# Using curl or Postman
curl -X POST http://localhost:5000/api/analyze/text \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "login admin delete database"}'
```

### Show Database
```bash
# MongoDB shell
use cyber_threat_detection
db.logs.find().pretty()
db.logs.aggregate([
  { $group: { _id: "$prediction", count: { $sum: 1 } } }
])
```

---

## 🎯 Key Takeaways

1. **AI-Powered**: Uses state-of-the-art Transformer models
2. **Real-time**: Instant threat detection
3. **User-Friendly**: Beautiful, intuitive interface
4. **Comprehensive**: Statistics, charts, alerts
5. **Scalable**: Modern tech stack (MERN + PyTorch)
6. **Secure**: JWT auth, encrypted passwords
7. **Flexible**: Configurable thresholds and models

---

**End Demo with Impact:**
> "This system demonstrates how AI can enhance cybersecurity by automatically detecting threats that humans might miss, helping organizations stay one step ahead of attackers."

🎉 **Demo Complete!**

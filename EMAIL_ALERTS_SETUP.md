# 📧 EMAIL ALERT NOTIFICATIONS SETUP GUIDE

## 🎯 **Overview**

Your Cyber Threat Detection System now sends **automatic email alerts** when suspicious or malicious activity is detected!

---

## ✅ **What You Get**

### **Automatic Alerts For**:
- 🚨 **Malicious Activity** - Critical threats
- ⚠️ **Suspicious Activity** - Potential threats
- ✅ **Normal Activity** - No alerts (optional)

### **Email Features**:
- 📧 **Beautiful HTML Emails** - Professional design
- 🎨 **Color-Coded** - Red (malicious), Orange (suspicious)
- 📊 **Detailed Information** - Event, confidence, timestamp, user
- 💡 **Recommended Actions** - Context-aware security steps
- 🔗 **Dashboard Links** - Quick access to view details

---

## 🔧 **Setup Instructions**

### **Step 1: Get Gmail App Password**

1. **Go to Google Account**:
   - Visit: https://myaccount.google.com/

2. **Enable 2-Step Verification**:
   - Security → 2-Step Verification → Turn On

3. **Generate App Password**:
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### **Step 2: Configure Backend .env File**

Open `backend/.env` and add these lines:

```bash
# Email Alerts Configuration
EMAIL_ALERTS_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
ALERT_RECIPIENTS=admin@company.com,security@company.com,you@gmail.com
```

**Replace**:
- `your-email@gmail.com` → Your Gmail address
- `abcd efgh ijkl mnop` → Your 16-character app password (no spaces)
- `admin@company.com,security@company.com,you@gmail.com` → Comma-separated list of recipients

### **Step 3: Restart Backend**

```bash
# Stop current backend (Ctrl+C)
# Then restart:
cd backend
venv\Scripts\python app.py
```

---

## 📝 **Configuration Options**

### **Environment Variables**:

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_ALERTS_ENABLED` | Enable/disable alerts | `true` or `false` |
| `SMTP_SERVER` | Mail server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` (TLS) |
| `SENDER_EMAIL` | Your email | `alerts@company.com` |
| `SENDER_PASSWORD` | App password | `abcd efgh ijkl mnop` |
| `ALERT_RECIPIENTS` | Who receives alerts | `admin@company.com,security@company.com` |

### **Multiple Recipients**:
```bash
# Separate with commas (no spaces)
ALERT_RECIPIENTS=admin@company.com,security@company.com,soc@company.com
```

---

## 🧪 **Testing Email Alerts**

### **Test 1: Single Malicious Log**

1. **Go to "Analyze Logs"**
2. **Enter**:
   ```
   admin login failed 10 times from unknown IP address
   ```
3. **Click "Analyze Log"**
4. **Check your email** - Should receive alert within seconds!

### **Test 2: Bulk Upload**

1. **Go to "Analyze Logs"**
2. **Upload** `test_data/malicious_logs.csv`
3. **Click "Analyze File"**
4. **Check your email** - Should receive 20 alerts!

### **Test 3: Verify Configuration**

**Option A: Check Backend Logs**
```
Look for:
✅ Alert email sent for malicious activity
OR
❌ Failed to send alert email: [error message]
```

**Option B: API Test** (Coming soon - admin endpoint)
```
POST /api/admin/email/test
```

---

## 📧 **Email Template Preview**

### **Subject**:
```
🚨 Security Alert: MALICIOUS Activity Detected
```

### **Content Includes**:
- 🎨 **Color-coded header** (red for malicious, orange for suspicious)
- 📝 **Event description**
- 🎯 **Threat level badge**
- 📊 **Confidence score**
- ⏰ **Timestamp**
- 👤 **User information**
- 🔍 **Processed sequence**
- 💡 **Recommended actions** (context-aware)
- 🔗 **Dashboard links**

---

## 🔒 **Security Best Practices**

### **Email Security**:
1. ✅ **Use App Passwords** - Never use your main Gmail password
2. ✅ **Dedicated Email** - Create `security-alerts@company.com`
3. ✅ **Limit Recipients** - Only send to security team
4. ✅ **Monitor Inbox** - Set up filters/rules for alerts

### **Gmail Settings**:
1. ✅ **Enable 2FA** - Required for app passwords
2. ✅ **Create Filter** - Auto-label security alerts
3. ✅ **Mobile Notifications** - Get instant alerts on phone
4. ✅ **Backup Recipients** - Add multiple team members

---

## 🎯 **Use Cases**

### **1. Real-Time Monitoring**:
```
- Security team receives instant alerts
- No need to constantly check dashboard
- Mobile notifications for urgent threats
```

### **2. Incident Response**:
```
- Email contains all details needed
- Recommended actions included
- Links to investigate in dashboard
```

### **3. Audit Trail**:
```
- Email history = permanent record
- Forward to incident response team
- Archive for compliance
```

### **4. Team Collaboration**:
```
- Multiple recipients get same alert
- Reply-all to coordinate response
- CC management for critical threats
```

---

## 🚨 **Alert Triggers**

### **Malicious Logs** (🚨 Critical):
- Admin login failures (10+ attempts)
- SQL injection attempts
- Privilege escalation
- Malware detection
- Data exfiltration
- Ransomware activity

### **Suspicious Logs** (⚠️ Warning):
- Login from new location
- Unusual time access (2-4 AM)
- Multiple failed attempts (3-9)
- Unusual data transfers
- Access to restricted files

### **Normal Logs** (✅ No Alert):
- Successful logins
- Regular file access
- Normal business hours activity
- Standard operations

---

## 🛠️ **Troubleshooting**

### **Problem: No Emails Received**

**Check 1: Configuration**
```bash
# Verify .env file
EMAIL_ALERTS_ENABLED=true  # Must be true!
SENDER_EMAIL=your-email@gmail.com  # Correct email?
SENDER_PASSWORD=abcd efgh ijkl mnop  # Correct app password?
```

**Check 2: Backend Logs**
```
Look for:
"Email alerts disabled or not configured"
"Failed to send alert email: [error]"
```

**Check 3: Gmail Settings**
- 2FA enabled?
- App password generated?
- Less secure apps NOT needed (app passwords work)

**Check 4: Spam Folder**
- Check spam/junk folder
- Mark as "Not Spam"
- Add sender to contacts

### **Problem: Authentication Failed**

**Solution**:
1. Regenerate app password
2. Copy without spaces: `abcdefghijklmnop`
3. Update `.env` file
4. Restart backend

### **Problem: Too Many Emails**

**Solution 1: Adjust Thresholds**
```bash
# In .env
SUSPICIOUS_THRESHOLD=0.7  # Higher = fewer alerts
MALICIOUS_THRESHOLD=0.85  # Higher = fewer alerts
```

**Solution 2: Filter Recipients**
```bash
# Only critical alerts
ALERT_RECIPIENTS=security-team@company.com
```

**Solution 3: Disable for Testing**
```bash
EMAIL_ALERTS_ENABLED=false
```

---

## 📊 **Email Statistics**

### **What to Expect**:
- **Delivery Time**: 1-5 seconds
- **Email Size**: ~15-20 KB (HTML)
- **Gmail Limit**: 500 emails/day (free), 2000/day (workspace)
- **Batch Uploads**: 1 email per suspicious/malicious log

### **Rate Limiting**:
If uploading large files:
- 100 logs = up to 100 emails
- Consider batching or summary emails for large uploads
- Gmail may delay if sending too fast

---

## 🎨 **Customization**

### **Change Email Template**:
Edit `backend/email_service.py`:
- Modify `_create_alert_html()` for custom design
- Change colors, layout, content
- Add company logo
- Customize recommendations

### **Change Recipients Per Alert Type**:
```python
# In email_service.py
if prediction == 'malicious':
    recipients = ['critical-team@company.com']
elif prediction == 'suspicious':
    recipients = ['monitoring-team@company.com']
```

---

## 📝 **Example .env Configuration**

```bash
# ==================== EMAIL ALERTS ====================

# Enable email notifications
EMAIL_ALERTS_ENABLED=true

# Gmail SMTP settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Sender credentials (use app password!)
SENDER_EMAIL=cyberguard-alerts@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop

# Who receives alerts (comma-separated, no spaces)
ALERT_RECIPIENTS=admin@company.com,security@company.com,soc-team@company.com

# ==================== OTHER SETTINGS ====================

# MongoDB
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=cyber_threat_detection

# JWT
JWT_SECRET_KEY=your-secret-key-here

# Thresholds
SUSPICIOUS_THRESHOLD=0.5
MALICIOUS_THRESHOLD=0.75
```

---

## 🎉 **You're All Set!**

### **Quick Start**:
1. ✅ Get Gmail app password
2. ✅ Update `backend/.env`
3. ✅ Restart backend
4. ✅ Test with malicious log
5. ✅ Check email inbox

### **Next Steps**:
- 📱 Set up mobile notifications
- 🔔 Create Gmail filters
- 👥 Add team members as recipients
- 📊 Monitor email delivery

**Your security team will now receive instant alerts! 📧🚨**

# 📧 EMAIL ALERTS - QUICK SETUP

## ✅ **Feature Added: Real-Time Email Notifications**

Your system now sends **automatic email alerts** when threats are detected!

---

## 🚀 **Quick Setup (5 Minutes)**

### **Step 1: Get Gmail App Password**

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Go to **App passwords**
4. Generate password for "Mail"
5. **Copy the 16-character code** (e.g., `abcdefghijklmnop`)

### **Step 2: Update .env File**

Open `backend/.env` and add:

```bash
# Email Alerts
EMAIL_ALERTS_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcdefghijklmnop
ALERT_RECIPIENTS=your-email@gmail.com,team@company.com
```

**Replace**:
- `your-email@gmail.com` → Your Gmail
- `abcdefghijklmnop` → Your app password (no spaces!)
- `your-email@gmail.com,team@company.com` → Who gets alerts

### **Step 3: Restart Backend**

Stop and restart the backend server.

### **Step 4: Test It!**

1. Go to "Analyze Logs"
2. Type: `admin login failed 10 times from unknown IP`
3. Click "Analyze Log"
4. **Check your email!** 📧

---

## 📧 **What You'll Receive**

### **Email Alerts Include**:
- 🎨 **Beautiful HTML Design** - Professional, color-coded
- 🚨 **Threat Level** - MALICIOUS (red) or SUSPICIOUS (orange)
- 📊 **Confidence Score** - How certain the AI is
- ⏰ **Timestamp** - When it happened
- 👤 **User Info** - Who triggered it
- 💡 **Recommended Actions** - What to do next
- 🔗 **Dashboard Link** - View details

### **Example Subject**:
```
🚨 Security Alert: MALICIOUS Activity Detected
```

---

## 🎯 **When Alerts Are Sent**

### **✅ Sends Email**:
- 🚨 **Malicious logs** - Critical threats
- ⚠️ **Suspicious logs** - Potential threats

### **❌ No Email**:
- ✅ **Normal logs** - Regular activity

---

## 🧪 **Test Scenarios**

### **Test 1: Single Alert**
```
Input: "admin login failed 10 times from unknown IP"
Result: 1 email sent (MALICIOUS)
```

### **Test 2: Bulk Upload**
```
Upload: test_data/malicious_logs.csv (20 logs)
Result: 20 emails sent (one per log)
```

### **Test 3: Mixed Logs**
```
Upload: test_data/realistic_mixed_logs.csv (30 logs)
Result: ~20 emails (only suspicious/malicious)
```

---

## ⚙️ **Configuration Options**

### **Disable Alerts**:
```bash
EMAIL_ALERTS_ENABLED=false
```

### **Multiple Recipients**:
```bash
# Comma-separated, no spaces
ALERT_RECIPIENTS=admin@company.com,security@company.com,soc@company.com
```

### **Change Email Provider**:
```bash
# For Outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# For custom SMTP
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587
```

---

## 🛠️ **Troubleshooting**

### **No Emails?**

**Check 1**: Is it enabled?
```bash
EMAIL_ALERTS_ENABLED=true  # Must be true!
```

**Check 2**: Correct credentials?
```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcdefghijklmnop  # No spaces!
```

**Check 3**: Backend logs
```
Look for:
✅ Alert email sent for malicious activity
OR
❌ Failed to send alert email: [error]
```

**Check 4**: Spam folder
- Check spam/junk
- Mark as "Not Spam"

---

## 📝 **Files Created**

1. **`backend/email_service.py`** - Email notification service
2. **`backend/.env.example`** - Updated with email config
3. **`EMAIL_ALERTS_SETUP.md`** - Complete setup guide (this file)

---

## 🎉 **You're Done!**

### **What Happens Now**:
1. ✅ System analyzes logs
2. ✅ Detects suspicious/malicious activity
3. ✅ **Sends instant email alert**
4. ✅ Security team responds immediately

### **Benefits**:
- 📱 **Mobile Notifications** - Get alerts on phone
- ⚡ **Instant Response** - No delay
- 📧 **Permanent Record** - Email history
- 👥 **Team Collaboration** - Multiple recipients

---

## 📚 **Full Documentation**

See `EMAIL_ALERTS_SETUP.md` for:
- Detailed Gmail setup
- Email template customization
- Advanced configuration
- Troubleshooting guide
- Best practices

---

## 🚨 **Example Alert Email**

```
Subject: 🚨 Security Alert: MALICIOUS Activity Detected

[Beautiful HTML Email with:]
- Red header with 🚨 icon
- Event: "admin login failed 10 times from unknown IP"
- Threat Level: MALICIOUS
- Confidence: 95.2%
- Timestamp: 2025-12-09 15:30:00
- User: admin@cyberguard.com

Recommended Actions:
🚨 Immediately isolate affected system
🔒 Disable compromised user account
📋 Review recent activity logs
🔍 Conduct forensic analysis
📞 Notify security team immediately

[View in Dashboard] [Go to Dashboard]
```

---

## ✅ **Quick Checklist**

- [ ] Get Gmail app password
- [ ] Update `backend/.env` file
- [ ] Set `EMAIL_ALERTS_ENABLED=true`
- [ ] Add your email to `SENDER_EMAIL`
- [ ] Add app password to `SENDER_PASSWORD`
- [ ] Add recipients to `ALERT_RECIPIENTS`
- [ ] Restart backend server
- [ ] Test with malicious log
- [ ] Check email inbox
- [ ] Set up mobile notifications

**Ready to receive real-time security alerts! 📧🚨**

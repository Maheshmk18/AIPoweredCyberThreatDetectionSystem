# Realistic Cybersecurity Log Datasets for Testing

## 📊 **Dataset 1: Normal User Activity (normal_logs.csv)**

```csv
event
user login successful from 192.168.1.100
file accessed during business hours
email sent to internal recipient
document saved successfully
user logout normal
application started successfully
database query executed
report generated for monthly review
password changed successfully
user session refreshed
file uploaded to shared drive
meeting scheduled in calendar
task completed successfully
backup completed successfully
system health check passed
user profile updated
notification sent successfully
data synchronized successfully
cache cleared successfully
settings updated successfully
```

## 🚨 **Dataset 2: Suspicious Activity (suspicious_logs.csv)**

```csv
event
user login from new location
file access at unusual time 2:30 AM
multiple failed authentication attempts
password change requested from unknown device
unusual data transfer volume detected
access attempt to restricted directory
database query at odd hours
file download from external IP
VPN connection from unusual country
privilege change request pending
account locked due to failed attempts
unusual network traffic pattern
multiple concurrent sessions detected
access to sensitive files after hours
configuration change without approval
unusual API calls detected
repeated access to same file
login from multiple locations simultaneously
data export request at midnight
system scan initiated unexpectedly
```

## 🔴 **Dataset 3: Malicious Activity (malicious_logs.csv)**

```csv
event
admin login failed 10 times from unknown IP address
database export initiated at 3:00 AM by unauthorized user
privilege escalation attempt detected
malware signature found in uploaded file
unauthorized access to restricted directory
SQL injection attempt blocked
brute force attack detected on admin account
ransomware activity detected
data exfiltration to external server
backdoor installation attempt blocked
credential dumping detected
lateral movement detected across network
suspicious PowerShell script execution
unauthorized service account creation
firewall rules modified without authorization
antivirus disabled by unknown process
registry modification detected
suspicious outbound connection to command server
mass file encryption detected
rootkit behavior detected
```

## 🎯 **Dataset 4: Mixed Realistic Logs (realistic_logs.csv)**

```csv
event
user john.doe login successful from 192.168.1.45
file quarterly_report.pdf accessed by jane.smith
admin login failed from IP 203.0.113.42
database backup completed successfully
user alice.wong logout normal
suspicious file download detected from external source
email sent to client@company.com
privilege escalation attempt by user bob.jones
document contract.docx saved successfully
malware signature detected in attachment.exe
user session timeout after 30 minutes
multiple failed login attempts for admin account
application update installed successfully
unauthorized access attempt to /etc/passwd
file upload to cloud storage completed
SQL injection detected in web form
system reboot scheduled for maintenance
brute force attack blocked from 198.51.100.23
user password reset requested
data exfiltration prevented to unknown server
meeting invite sent successfully
ransomware activity detected and quarantined
backup verification passed
credential theft attempt blocked
user profile picture updated
suspicious network scan detected
report generated for Q4 analysis
unauthorized API access attempt
cache cleared automatically
firewall blocked connection to malicious IP
```

## 🌐 **Dataset 5: Network Security Logs (network_logs.csv)**

```csv
event
firewall allowed connection from trusted IP 192.168.1.50
port scan detected from external IP 203.0.113.15
VPN connection established successfully
DDoS attack detected and mitigated
SSL certificate validated successfully
intrusion detection system alert triggered
network traffic spike detected
DNS query to suspicious domain blocked
packet loss detected on network interface
bandwidth threshold exceeded
unauthorized port opening attempt
network segmentation violation detected
ARP spoofing attempt blocked
man-in-the-middle attack prevented
network device configuration changed
unauthorized SNMP access attempt
network performance degraded
suspicious DNS tunneling detected
firewall rule violation logged
network device firmware updated
```

## 📁 **How to Use These Datasets**

### **Method 1: Copy & Paste**
1. Go to "Analyze Logs" page
2. Copy any log from above
3. Paste into "Single Log Analysis"
4. Click "Analyze Log"

### **Method 2: Create CSV Files**
1. Create a new file (e.g., `test_logs.csv`)
2. Copy the CSV content from any dataset above
3. Save the file
4. Go to "Analyze Logs" page
5. Upload the CSV file
6. Click "Analyze File"

### **Method 3: Mix and Match**
Create your own CSV with mixed logs:
```csv
event
user login successful from office
admin login failed 5 times from unknown IP
file accessed normally
database export at 3 AM suspicious
email sent successfully
malware detected in download
```

---

## 🎯 **Expected Results**

### **Normal Logs** → Should predict: `normal` (70-95% confidence)
### **Suspicious Logs** → Should predict: `suspicious` (60-85% confidence)
### **Malicious Logs** → Should predict: `malicious` (80-98% confidence)

---

## 🧪 **Testing Scenarios**

### **Scenario 1: Test Single Log**
```
Input: "admin login failed 10 times from unknown IP"
Expected: MALICIOUS (90%+ confidence)
```

### **Scenario 2: Test File Upload**
```
Upload: malicious_logs.csv (20 logs)
Expected: 
- Total: 20
- Malicious: 18-20
- Suspicious: 0-2
- Normal: 0
```

### **Scenario 3: Test Mixed Logs**
```
Upload: realistic_logs.csv (30 logs)
Expected:
- Total: 30
- Normal: ~10
- Suspicious: ~10
- Malicious: ~10
```

---

## 💡 **Pro Tips**

1. **Start Small**: Test with 5-10 logs first
2. **Check Confidence**: Higher scores = more certain
3. **Review Alerts**: Malicious logs appear in Alerts page
4. **Role Testing**: Login as different roles to see filtered views
5. **Investigate**: Click "Investigate" on alerts for details

---

## 📝 **Quick Test Commands**

### **Test 1: Normal Activity**
```
user login successful from 192.168.1.100
```
Expected: NORMAL

### **Test 2: Suspicious Activity**
```
user login from new location at 2 AM
```
Expected: SUSPICIOUS

### **Test 3: Malicious Activity**
```
admin login failed 10 times from unknown IP address
```
Expected: MALICIOUS

---

**Save these datasets and use them to thoroughly test your cybersecurity system! 🛡️**

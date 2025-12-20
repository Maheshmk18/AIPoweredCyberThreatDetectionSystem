"""
Email notification service for sending alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.alert_recipients = os.getenv('ALERT_RECIPIENTS', '').split(',')
        self.enabled = os.getenv('EMAIL_ALERTS_ENABLED', 'false').lower() == 'true'
    
    def send_alert_email(self, log_data):
        """Send email notification for suspicious/malicious logs"""
        if not self.enabled or not self.sender_email:
            print("Email alerts disabled or not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚨 Security Alert: {log_data['prediction'].upper()} Activity Detected"
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.alert_recipients)
            
            # Create HTML email body
            html_body = self._create_alert_html(log_data)
            
            # Attach HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Alert email sent for {log_data['prediction']} activity")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send alert email: {e}")
            return False
    
    def _create_alert_html(self, log_data):
        """Create HTML email template for alerts"""
        severity_colors = {
            'malicious': '#dc2626',
            'suspicious': '#f59e0b',
            'normal': '#10b981'
        }
        
        severity_icons = {
            'malicious': '🚨',
            'suspicious': '⚠️',
            'normal': '✅'
        }
        
        color = severity_colors.get(log_data['prediction'], '#6b7280')
        icon = severity_icons.get(log_data['prediction'], '📊')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f3f4f6;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 700;
                }}
                .header .icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                }}
                .content {{
                    padding: 30px;
                }}
                .alert-box {{
                    background-color: #f9fafb;
                    border-left: 4px solid {color};
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .detail-row {{
                    margin: 15px 0;
                    padding: 10px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                .detail-row:last-child {{
                    border-bottom: none;
                }}
                .label {{
                    font-weight: 600;
                    color: #374151;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 5px;
                }}
                .value {{
                    color: #1f2937;
                    font-size: 16px;
                    word-break: break-word;
                }}
                .confidence {{
                    display: inline-block;
                    background-color: {color};
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 14px;
                }}
                .footer {{
                    background-color: #f9fafb;
                    padding: 20px;
                    text-align: center;
                    color: #6b7280;
                    font-size: 14px;
                }}
                .footer a {{
                    color: {color};
                    text-decoration: none;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="icon">{icon}</div>
                    <h1>{log_data['prediction'].upper()} Activity Detected</h1>
                </div>
                
                <div class="content">
                    <div class="alert-box">
                        <div class="detail-row">
                            <div class="label">Event Description</div>
                            <div class="value">{log_data['event']}</div>
                        </div>
                        
                        <div class="detail-row">
                            <div class="label">Threat Level</div>
                            <div class="value">
                                <span class="confidence">{log_data['prediction'].upper()}</span>
                            </div>
                        </div>
                        
                        <div class="detail-row">
                            <div class="label">Confidence Score</div>
                            <div class="value">{(log_data['score'] * 100):.1f}%</div>
                        </div>
                        
                        <div class="detail-row">
                            <div class="label">Timestamp</div>
                            <div class="value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                        </div>
                        
                        {f'''
                        <div class="detail-row">
                            <div class="label">User</div>
                            <div class="value">{log_data.get('user_email', 'System')}</div>
                        </div>
                        ''' if log_data.get('user_email') else ''}
                        
                        <div class="detail-row">
                            <div class="label">Processed Sequence</div>
                            <div class="value" style="font-family: monospace; font-size: 14px; background: #f3f4f6; padding: 10px; border-radius: 4px;">
                                {log_data['sequence']}
                            </div>
                        </div>
                    </div>
                    
                    <h3 style="color: #374151; margin-top: 30px;">Recommended Actions:</h3>
                    <ul style="color: #4b5563; line-height: 1.8;">
                        {self._get_recommendations(log_data['prediction'])}
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from CyberGuard Threat Detection System</p>
                    <p>
                        <a href="http://localhost:3000/alerts">View in Dashboard</a> | 
                        <a href="http://localhost:3000/dashboard">Go to Dashboard</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _get_recommendations(self, prediction):
        """Get recommended actions based on threat level"""
        if prediction == 'malicious':
            return """
                <li>🚨 Immediately isolate the affected system</li>
                <li>🔒 Disable compromised user account</li>
                <li>📋 Review recent activity logs</li>
                <li>🔍 Conduct forensic analysis</li>
                <li>📞 Notify security team immediately</li>
                <li>🛡️ Check for lateral movement</li>
            """
        elif prediction == 'suspicious':
            return """
                <li>⚠️ Monitor user activity closely</li>
                <li>📊 Review related logs for patterns</li>
                <li>🔍 Investigate source IP/location</li>
                <li>📝 Document findings</li>
                <li>👁️ Set up additional monitoring</li>
            """
        else:
            return """
                <li>✅ No immediate action required</li>
                <li>📊 Continue normal monitoring</li>
            """
    
    def test_connection(self):
        """Test email configuration"""
        if not self.enabled:
            return {'success': False, 'message': 'Email alerts are disabled'}
        
        if not self.sender_email or not self.sender_password:
            return {'success': False, 'message': 'Email credentials not configured'}
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
            return {'success': True, 'message': 'Email configuration is valid'}
        except Exception as e:
            return {'success': False, 'message': f'Connection failed: {str(e)}'}

# Create global email service instance
email_service = EmailService()

# 🛡️ AI-Powered Cyber Threat Detection System: End-to-End Explanation

## 1. Project Overview
This project is an **Enterprise-Grade Security Information and Event Management (SIEM)** tool enhanced with Artificial Intelligence. Unlike traditional firewalls that rely on fixed rules, this system uses **Machine Learning (NLP)** to "read" and understand computer logs, detecting new and unknown threats (Zero-Day attacks) in real-time.

---

## 2. Technical Architecture
The system follows a modern **Decoupled Architecture**:

*   **Frontend (The Face)**: Built with **React.js**. It provides a beautiful, responsive 3D dashboard for users to interact with the system.
*   **Backend (The Brain)**: Built with **Python Flask**. It acts as the API server that handles all logic, authentication, and communication.
*   **AI Engine (The Intelligence)**: Powered by **Hugging Face Transformers (DistilBERT)**. A deep learning model that understands the context of text logs.
*   **Database (The Memory)**: **MongoDB Atlas**. A cloud-based NoSQL database to store millions of logs and user data efficiently.
*   **Notification System (The Action)**: **SMTP Email Service**. Sends instant alerts when critical threats are found.

---

## 3. End-to-End Workflow (How it Works)

### **Step 1: User Entry & Authentication**
*   The user lands on a stunning **Landing Page** featuring 3D animations and information about the system.
*   They click **"Get Started"** to access the login page.
*   **JWT Security**: When they log in, the system verifies credentials. If valid, it issues a **JSON Web Token (JWT)**. This token is like a digital ID card attached to every subsequent request, ensuring the session is secure.

### **Step 2: The Dashboard**
*   Upon login, the user sees a **Real-Time Dashboard**.
*   It displays live statistics: Total Logs, Threat Counts (Normal vs Malicious), and visual charts.
*   *Note: In our demo, we implemented a robust "Offline Mode" that mocks this data if the database is temporarily unreachable.*

### **Step 3: Log Input & Analysis**
The core functionality happens here. The user has two ways to check for threats:
1.  **Direct Input**: Typing a log message (e.g., "admin failed login").
2.  **Bulk Upload**: Uploading a CSV/Log file with thousands of entries.

### **Step 4: Backend Processing & AI Prediction**
When a log is submitted:
1.  **Preprocessing**: The backend takes the raw text and "tokenizes" it (turns words into numbers that the AI can read).
2.  **DistilBERT Model**: These numbers are fed into the **Transformer Model**.
3.  **Context Understanding**: The AI doesn't just look for keywords like "error"; it understands **context**.
    *   *Example*: "User forgot password" -> **Normal**.
    *   *Example*: "User failed password 50 times in 1 second" -> **Malicious**.
4.  **Classification**: The model outputs a probability score and classifies the log as **Normal, Suspicious, or Malicious**.

### **Step 5: Database & Persistence**
*   The system saves the log, its classification, and the AI confidence score into **MongoDB**.
*   This creates an audit trail for future investigations.

### **Step 6: Automated Response (Email Alert)**
*   If the AI classifies a log as **"Malicious"** or **"Suspicious"**, the **Email Service** kicks in.
*   It instantly constructs an HTML email containing the threat details.
*   It sends this alert to the Admin (SOC Team), enabling immediate action.

---

## 4. Key Features & Innovations

*   **Deep Learning vs Rule-Based**: Most systems just search for "error". Our system understands natural language, making it smarter against hackers who try to hide.
*   **Zero-Latency Interface**: The React frontend is optimized for speed, providing instant feedback.
*   **Fault Tolerance**: The system is designed to handle database failures gracefully without crashing, ensuring the UI remains accessible.
*   **Role-Based Access Control (RBAC)**: Different views for Admins (who control everything) vs Normal Users.

---

## 5. Conclusion
This project demonstrates the convergence of **Cybersecurity** and **Modern AI**. It solves the problem of "Alert Fatigue" by automating the analysis process and ensuring only relevant, high-confidence threats reach the human operators.

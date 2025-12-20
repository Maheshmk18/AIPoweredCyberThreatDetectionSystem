# Cyber Threat Detection System - Setup Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- MongoDB (local or Atlas)

### Step 1: MongoDB Setup

#### Option A: Local MongoDB
1. Install MongoDB from https://www.mongodb.com/try/download/community
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo systemctl start mongod
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Update `backend/.env` with your connection string

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env and update MongoDB connection if needed

# Run the backend server
python app.py
```

The backend will start on `http://localhost:5000`

### Step 3: Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will start on `http://localhost:3000`

### Step 4: Create First User

1. Open browser to `http://localhost:3000`
2. Click "Register" tab
3. Enter email and password
4. Click "Register"
5. Switch to "Login" tab and login

### Step 5: Test the System

1. **Upload Sample Logs**:
   - Click "Choose file" in the Upload section
   - Select `sample_logs.csv` from the project root
   - Click "Analyze File"
   - Wait for analysis to complete

2. **Analyze Text**:
   - Enter: `login admin delete database export`
   - Click "Analyze Text"
   - See the malicious prediction

3. **View Dashboard**:
   - See statistics and charts
   - Browse recent logs table

4. **View Alerts**:
   - Click "View Alerts" button
   - See all malicious activities

## 🧠 Training the Model (Optional)

To train the model on your own data:

```bash
cd backend/model
python train_model.py
```

This will create a `threat_detection_model.pth` file that will be automatically loaded.

## 📊 Understanding Predictions

- **Normal** (Green): Regular user behavior
- **Suspicious** (Yellow): Potentially concerning activity
- **Malicious** (Red): High-risk threat detected

## 🔧 Troubleshooting

### Backend Issues

**MongoDB Connection Error**:
- Ensure MongoDB is running
- Check connection string in `.env`
- Verify network access (for Atlas)

**Module Not Found**:
```bash
pip install -r requirements.txt
```

**Port 5000 Already in Use**:
- Change port in `app.py`: `app.run(port=5001)`
- Update frontend `.env`: `REACT_APP_API_URL=http://localhost:5001/api`

### Frontend Issues

**Dependencies Error**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**API Connection Error**:
- Ensure backend is running
- Check `.env` has correct API URL
- Check browser console for CORS errors

## 🎯 Next Steps

1. **Add More Training Data**: Update `preprocessor.py` with more examples
2. **Fine-tune Model**: Run `train_model.py` with your data
3. **Customize Thresholds**: Adjust in `config.py`
4. **Add More Features**: Extend the API and UI

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify token

### Analysis
- `POST /api/analyze/text` - Analyze text log
- `POST /api/analyze/file` - Analyze file upload

### Logs
- `GET /api/logs` - Get all logs
- `GET /api/logs/malicious` - Get malicious logs
- `GET /api/logs/filter/:prediction` - Filter by prediction
- `GET /api/statistics` - Get statistics
- `DELETE /api/logs/:id` - Delete log
- `DELETE /api/logs/clear` - Clear all logs

## 🔐 Security Notes

- Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting
- Add input validation
- Use environment variables for sensitive data

## 🎨 Customization

### Change Model
Edit `config.py`:
```python
MODEL_NAME = 'bert-base-uncased'  # or 'roberta-base'
```

### Adjust Thresholds
Edit `config.py`:
```python
SUSPICIOUS_THRESHOLD = 0.6
MALICIOUS_THRESHOLD = 0.8
```

### Modify UI Colors
Edit `frontend/src/index.css` CSS variables

## 📝 License

This project is for educational purposes.

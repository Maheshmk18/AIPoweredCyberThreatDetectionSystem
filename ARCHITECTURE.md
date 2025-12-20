# 🏗️ Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (React)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Login   │  │Dashboard │  │  Alerts  │  │ Analytics│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (Flask)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │ Analysis │  │   Logs   │  │  Stats   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   AI MODEL (PyTorch)     │  │   DATABASE (MongoDB)     │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ Transformer Model  │  │  │  │  Users Collection  │  │
│  │  (DistilBERT)      │  │  │  │  Logs Collection   │  │
│  └────────────────────┘  │  │  └────────────────────┘  │
└──────────────────────────┘  └──────────────────────────┘
```

## Component Breakdown

### 🎨 Frontend (React)

#### Pages
1. **Login.js** (`/`)
   - User authentication (login/register)
   - JWT token management
   - Beautiful glassmorphism UI

2. **Dashboard.js** (`/dashboard`)
   - Statistics overview
   - File upload interface
   - Text analysis input
   - Interactive charts (Bar, Pie)
   - Recent logs table

3. **Alerts.js** (`/alerts`)
   - Malicious activity alerts
   - Detailed threat information
   - Alert management (delete)

#### Services
- **api.js**: Axios-based API client
  - Authentication methods
  - Log analysis methods
  - Token interceptor

#### Styling
- **index.css**: Global styles with CSS variables
- **Component CSS**: Page-specific styles
- Dark theme with gradient accents
- Smooth animations and transitions

### ⚙️ Backend (Flask)

#### Core Files

1. **app.py** - Main Flask application
   - Route definitions
   - Request handling
   - Error handling
   - CORS configuration

2. **auth.py** - Authentication module
   - User registration
   - Login with JWT
   - Token verification
   - Password hashing (bcrypt)

3. **database.py** - MongoDB interface
   - User operations
   - Log CRUD operations
   - Statistics aggregation
   - Index management

4. **config.py** - Configuration
   - Environment variables
   - Model settings
   - Thresholds
   - Database connection

#### Model Package

1. **transformer_model.py** - AI Model
   - ThreatDetectionModel class
   - BERT/DistilBERT integration
   - Prediction logic
   - Heuristic rules

2. **preprocessor.py** - Data preprocessing
   - Text cleaning
   - Sequence extraction
   - CSV parsing
   - Training data generation

3. **train_model.py** - Model training
   - Dataset creation
   - Training loop
   - Validation
   - Model saving

### 🗄️ Database Schema

#### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password_hash: Binary,
  created_at: DateTime
}
```

#### Logs Collection
```javascript
{
  _id: ObjectId,
  event: String,           // Original log text
  sequence: String,        // Processed sequence
  prediction: String,      // "normal" | "suspicious" | "malicious"
  score: Float,           // Confidence score (0-1)
  timestamp: DateTime,
  user_email: String
}
```

## 🔄 Data Flow

### 1. User Authentication
```
User → Login Form → POST /api/auth/login → Verify Password
  → Generate JWT → Store Token → Redirect to Dashboard
```

### 2. File Upload Analysis
```
User → Upload CSV → POST /api/analyze/file → Parse CSV
  → Extract Sequences → Transformer Prediction → Save to DB
  → Return Results → Update Dashboard
```

### 3. Text Analysis
```
User → Enter Text → POST /api/analyze/text → Preprocess
  → Transformer Prediction → Save to DB → Return Result
```

### 4. Dashboard Load
```
Dashboard → GET /api/statistics + GET /api/logs
  → Fetch from MongoDB → Render Charts & Tables
```

## 🧠 AI Model Architecture

### Transformer Pipeline

```
Input Text: "login admin delete database"
     ↓
[Preprocessing]
  - Lowercase
  - Remove special chars
  - Extract keywords
     ↓
Sequence: "login admin delete database"
     ↓
[Tokenization]
  - DistilBERT Tokenizer
  - Max length: 128
  - Padding & Truncation
     ↓
Token IDs: [101, 7164, 3968, ...]
     ↓
[Transformer Model]
  - DistilBERT Base
  - 6 layers, 768 hidden size
  - Self-attention mechanism
     ↓
[CLS] Token Embedding: [768-dim vector]
     ↓
[Classification Head]
  - Dropout (0.3)
  - Linear layer (768 → 3)
     ↓
Logits: [0.1, 0.2, 0.7]
     ↓
[Softmax]
     ↓
Probabilities: {
  normal: 0.05,
  suspicious: 0.15,
  malicious: 0.80
}
     ↓
[Heuristic Enhancement]
  - Keyword matching
  - Pattern detection
     ↓
Final Prediction: "malicious" (92%)
```

### Heuristic Rules

**Malicious Keywords:**
- delete, admin, root, sudo
- export, database, privilege
- escalation, unauthorized, brute

**Suspicious Keywords:**
- failed, denied, attempt
- retry, error, forbidden

**Scoring Logic:**
- 2+ malicious keywords → Malicious (75-98%)
- 1 malicious + 1 suspicious → Malicious (70-95%)
- 2+ suspicious keywords → Suspicious (55-85%)
- Otherwise → Normal (40-60%)

## 🔐 Security Features

1. **Authentication**
   - JWT tokens (24h expiry)
   - Bcrypt password hashing
   - Protected routes

2. **API Security**
   - CORS enabled
   - Token verification
   - Input validation

3. **Database**
   - Indexed queries
   - Unique email constraint
   - Connection pooling

## 📊 Visualization Components

### Recharts Integration

1. **Bar Chart** - Threat distribution
   - X-axis: Categories (Normal, Suspicious, Malicious)
   - Y-axis: Count
   - Color-coded bars

2. **Pie Chart** - Threat breakdown
   - Percentage distribution
   - Interactive tooltips
   - Custom colors

3. **Statistics Cards**
   - Total logs
   - Category counts
   - Icon indicators

## 🚀 Performance Optimizations

1. **Frontend**
   - Lazy loading
   - Memoization
   - Debounced inputs
   - Pagination (limit 100)

2. **Backend**
   - Database indexing
   - Batch processing
   - Model caching
   - Connection pooling

3. **Model**
   - GPU acceleration (if available)
   - Batch inference
   - Cached tokenizer

## 🔧 Configuration Options

### Model Selection
```python
# config.py
MODEL_NAME = 'distilbert-base-uncased'  # Fast, efficient
# MODEL_NAME = 'bert-base-uncased'      # More accurate
# MODEL_NAME = 'roberta-base'           # Best performance
```

### Thresholds
```python
SUSPICIOUS_THRESHOLD = 0.5   # 50% confidence
MALICIOUS_THRESHOLD = 0.75   # 75% confidence
```

### Database
```python
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'cyber_threat_detection'
```

## 📈 Scalability Considerations

### Current Limitations
- Single server deployment
- In-memory model loading
- No caching layer

### Future Enhancements
1. **Horizontal Scaling**
   - Load balancer
   - Multiple API servers
   - Shared model service

2. **Caching**
   - Redis for sessions
   - Model prediction cache
   - Query result cache

3. **Queue System**
   - Celery for async tasks
   - Batch file processing
   - Background training

4. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)

## 🧪 Testing Strategy

### Unit Tests
- Model predictions
- Preprocessing logic
- API endpoints
- Database operations

### Integration Tests
- End-to-end flows
- Authentication
- File upload
- Data persistence

### Performance Tests
- Load testing (100+ concurrent users)
- Large file uploads (10MB+)
- Database query optimization

## 📦 Deployment

### Development
```bash
# Backend
cd backend && python app.py

# Frontend
cd frontend && npm start
```

### Production
```bash
# Backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
npm run build
# Serve with nginx or similar
```

### Docker (Future)
```yaml
services:
  backend:
    build: ./backend
    ports: ["5000:5000"]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  
  mongodb:
    image: mongo:latest
    ports: ["27017:27017"]
```

## 🎯 Key Features Summary

✅ JWT Authentication
✅ Transformer-based AI (BERT/DistilBERT)
✅ Real-time threat detection
✅ Interactive dashboard
✅ File upload (CSV, TXT, LOG)
✅ Text analysis
✅ Statistics & charts
✅ Alert management
✅ MongoDB persistence
✅ Responsive UI
✅ Dark theme
✅ Smooth animations

## 📚 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI framework |
| Routing | React Router | Navigation |
| Charts | Recharts | Data visualization |
| Icons | Lucide React | Icon library |
| HTTP | Axios | API client |
| Backend | Flask | Web framework |
| Auth | JWT Extended | Authentication |
| Database | MongoDB | Data storage |
| ODM | PyMongo | MongoDB driver |
| ML | PyTorch | Deep learning |
| NLP | Transformers | Pre-trained models |
| Tokenizer | HuggingFace | Text processing |
| Security | Bcrypt | Password hashing |

---

**Built with ❤️ for Cybersecurity**

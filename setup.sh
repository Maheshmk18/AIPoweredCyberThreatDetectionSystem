#!/bin/bash

echo "========================================"
echo "Cyber Threat Detection System - Setup"
echo "========================================"
echo ""

echo "[1/4] Setting up Backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Copying environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please update MongoDB connection if needed."
else
    echo ".env file already exists."
fi

echo ""
echo "[2/4] Setting up Frontend..."
cd ../frontend

echo "Installing Node.js dependencies..."
npm install

echo ""
echo "[3/4] Setup Complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Make sure MongoDB is running"
echo "   - Local: sudo systemctl start mongod"
echo "   - Or use MongoDB Atlas (cloud)"
echo ""
echo "2. Start the Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. Start the Frontend (in new terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. Open browser to http://localhost:3000"
echo ""
echo "========================================"
echo "For detailed instructions, see SETUP_GUIDE.md"
echo "========================================"
echo ""

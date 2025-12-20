#!/bin/bash

echo "========================================"
echo "Starting Cyber Threat Detection System"
echo "========================================"
echo ""

echo "[1/3] Starting MongoDB..."
sudo systemctl start mongod
if [ $? -ne 0 ]; then
    echo "MongoDB failed to start or is already running"
    echo "Please ensure MongoDB is running before continuing"
    read -p "Press enter to continue..."
fi

echo ""
echo "[2/3] Starting Backend Server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 5

echo ""
echo "[3/3] Starting Frontend Server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "System Started!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user interrupt
wait

@echo off
echo ========================================
echo Starting Cyber Threat Detection System
echo ========================================
echo.

echo [1/3] Starting MongoDB...
net start MongoDB
if %errorlevel% neq 0 (
    echo MongoDB is already running or not installed
    echo Please ensure MongoDB is running before continuing
    pause
)

echo.
echo [2/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo System Starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two new windows will open:
echo 1. Backend Server (Flask)
echo 2. Frontend Server (React)
echo.
echo Your browser will open automatically to:
echo http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul

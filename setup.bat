@echo off
echo ========================================
echo Cyber Threat Detection System - Setup
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Copying environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please update MongoDB connection if needed.
) else (
    echo .env file already exists.
)

echo.
echo [2/4] Setting up Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo [3/4] Setup Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Make sure MongoDB is running
echo    - Local: net start MongoDB
echo    - Or use MongoDB Atlas (cloud)
echo.
echo 2. Start the Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 3. Start the Frontend (in new terminal):
echo    cd frontend
echo    npm start
echo.
echo 4. Open browser to http://localhost:3000
echo.
echo ========================================
echo For detailed instructions, see SETUP_GUIDE.md
echo ========================================
echo.
pause

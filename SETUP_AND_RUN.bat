@echo off
echo ============================================
echo CYBER THREAT DETECTION SYSTEM - SETUP
echo ============================================
echo.

echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.

echo Step 2: Checking MongoDB Configuration...
echo.
echo IMPORTANT: You need to configure MongoDB first!
echo.
echo Option 1 - MongoDB Atlas (Recommended - Free):
echo   1. Go to https://www.mongodb.com/cloud/atlas
echo   2. Create free account and cluster
echo   3. Get connection string
echo   4. Update backend\.env file with:
echo      MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
echo.
echo Option 2 - Local MongoDB:
echo   1. Install MongoDB locally
echo   2. Start MongoDB service
echo   3. Use: MONGO_URI=mongodb://localhost:27017/
echo.

set /p CONTINUE="Have you configured MongoDB? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo.
    echo Please configure MongoDB first, then run this script again.
    pause
    exit /b 0
)

echo.
echo Step 3: Installing Backend Dependencies...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Step 4: Initializing Demo Data...
python init_demo.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to initialize demo data.
    echo Please check your MongoDB connection in backend\.env
    pause
    exit /b 1
)

echo.
echo ============================================
echo SETUP COMPLETE!
echo ============================================
echo.
echo Demo Credentials:
echo   Admin: admin@cyberguard.com / Admin@123
echo   SOC:   soc@cyberguard.com / SOC@123
echo   User:  user@cyberguard.com / User@123
echo.
echo Next Steps:
echo   1. Run: start_backend.bat (in new terminal)
echo   2. Run: start_frontend.bat (in another terminal)
echo   3. Open: http://localhost:3000
echo.
pause

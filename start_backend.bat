@echo off
echo ============================================
echo STARTING BACKEND SERVER
echo ============================================
echo.

cd backend
call venv\Scripts\activate

echo Starting Flask backend on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

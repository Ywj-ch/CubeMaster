@echo off
chcp 65001 >nul
echo ================================
echo  CubeMaster Backend Server
echo ================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Navigate to backend directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in backend directory
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found in backend directory
    pause
    exit /b 1
)

REM Check if uvicorn is installed
python -c "import uvicorn" >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] uvicorn is not installed
    echo [INFO] Installing dependencies from requirements.txt...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] Dependencies installed successfully
    echo.
)

echo [SUCCESS] Starting FastAPI server...
echo [INFO] Server will run at: http://localhost:8000
echo [INFO] API documentation: http://localhost:8000/docs
echo [INFO] Press Ctrl+C to stop the server
echo.
echo --------------------------------
echo.

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

REM If server stops
echo.
echo [INFO] Server has stopped
pause

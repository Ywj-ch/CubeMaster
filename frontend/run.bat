@echo off
chcp 65001 >nul
echo ================================
echo  CubeMaster Frontend Server
echo ================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Navigate to frontend directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%
echo.

REM Check if package.json exists
if not exist "package.json" (
    echo [ERROR] package.json not found in frontend directory
    echo Make sure you are in the correct directory
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist "node_modules\" (
    echo [WARNING] node_modules not found
    echo [INFO] Running npm install to install dependencies...
    echo.
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed
        pause
        exit /b 1
    )
    echo.
    echo [SUCCESS] Dependencies installed successfully
    echo.
)

echo [SUCCESS] Starting Vite development server...
echo [INFO] Server will run at: http://localhost:5173
echo [INFO] Press Ctrl+C to stop the server
echo.
echo --------------------------------
echo.

call npm run dev

REM If server stops
echo.
echo [INFO] Server has stopped
pause

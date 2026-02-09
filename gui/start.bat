@echo off
REM Statscrypt Suite Startup Script for Windows
REM This script will install dependencies and start the Electron app

echo ==========================================
echo   Statscrypt Suite - Startup Script
echo ==========================================
echo.

REM Check if Node.js is installed
echo [*] Checking for Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do echo [OK] Node.js found: %%i

REM Check if npm is installed
echo [*] Checking for npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do echo [OK] npm found: %%i

REM Check if node_modules exists
echo [*] Checking dependencies...
if not exist node_modules (
    echo [*] Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.
echo [*] Starting Statscrypt Suite...
echo.

REM Start the app
call npm start

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start the application
    pause
)

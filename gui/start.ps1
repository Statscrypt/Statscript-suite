# Statscrypt Suite Startup Script for Windows
# This script will install dependencies and start the Electron app

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Statscrypt Suite - Startup Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "[*] Checking for Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    Pause
    exit 1
}

# Check if npm is installed
Write-Host "[*] Checking for npm..." -ForegroundColor Yellow
$npmVersion = npm --version 2>$null
if ($npmVersion) {
    Write-Host "[OK] npm found: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] npm is not installed" -ForegroundColor Red
    Pause
    exit 1
}

# Check if node_modules exists
Write-Host "[*] Checking dependencies..." -ForegroundColor Yellow
if (-Not (Test-Path "node_modules")) {
    Write-Host "[*] Installing npm dependencies..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        Pause
        exit 1
    }
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[OK] Dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "[*] Starting Statscrypt Suite..." -ForegroundColor Cyan
Write-Host ""


npm start

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to start the application" -ForegroundColor Red
    Pause
}

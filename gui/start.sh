#!/bin/bash
# Statscrypt Suite Startup Script for macOS and Linux

echo "=========================================="
echo "  Statscrypt Suite - Startup Script"
echo "=========================================="
echo ""

# Check if Node.js is installed
echo "[*] Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi
echo "[OK] Node.js found: $(node --version)"

# Check if npm is installed
echo "[*] Checking for npm..."
if ! command -v npm &> /dev/null; then
    echo "[ERROR] npm is not installed"
    exit 1
fi
echo "[OK] npm found: $(npm --version)"

# Check if node_modules exists
echo "[*] Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "[*] Installing npm dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[OK] Dependencies installed"
else
    echo "[OK] Dependencies already installed"
fi

echo ""
echo "[*] Starting Statscrypt Suite..."
echo ""

# Start the app
npm start

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to start the application"
    exit 1
fi

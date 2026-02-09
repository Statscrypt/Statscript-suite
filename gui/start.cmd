@echo off
REM Statscrypt Suite - Windows Bootstrap
REM Installs just (if needed) and starts the app
REM Works from Command Prompt or PowerShell

setlocal enabledelayedexpansion

echo ===========================================
echo   Statscrypt Suite - Bootstrap
echo ===========================================
echo.

REM Check if just is installed
for /f "delims=" %%i in ('where just 2^>nul') do set "JUST_PATH=%%i"

if not defined JUST_PATH (
    echo [*] 'just' task runner not found. Installing...
    echo.
    
    REM Try to install just using cargo
    for /f "delims=" %%i in ('where cargo 2^>nul') do set "CARGO_PATH=%%i"
    
    if defined CARGO_PATH (
        echo Installing just via cargo...
        cargo install just
        if errorlevel 1 (
            echo [!] Cargo installation failed
            goto install_failed
        )
    ) else (
        REM Try downloading prebuilt binary
        echo Installing just from GitHub...
        echo Downloading installer...
        
        powershell -Command "^
            try {^
                $arch = if ([Environment]::Is64BitProcess) { 'x86_64' } else { 'i686' };^
                $url = 'https://github.com/casey/just/releases/download/1.14.0/just-1.14.0-' + $arch + '-pc-windows-msvc.zip';^
                $output = '%TEMP%\just-win.zip';^
                [Net.ServicePointManager]::SecurityProtocol = 'tls12';^
                (New-Object System.Net.WebClient).DownloadFile($url, $output);^
                Expand-Archive -Path $output -DestinationPath '%APPDATA%'\Microsoft\Windows\Start Menu\Programs\Startup;^
                Write-Host '[OK] just extracted';^
            } catch {^
                Write-Host '[ERROR] Download failed: $_';^
                exit 1;^
            }^
        "
        if errorlevel 1 (
            echo.
            echo [!] Automatic installation failed.
            echo.
            echo Please install 'just' manually:
            echo   1. Download from: https://github.com/casey/just/releases
            echo   2. Extract just.exe to: C:\Windows\System32
            echo   3. Run this script again
            echo.
            pause
            exit /b 1
        )
    )
    
    echo [OK] just installed successfully
    echo.
)

REM Verify just is now available
where just >nul 2>&1
if errorlevel 1 (
    echo [ERROR] just still not found after installation
    pause
    exit /b 1
)

for /f "delims=" %%i in ('just --version') do echo [OK] %%i
echo.
echo Starting Statscrypt Suite...
echo.

REM Start the app
cd /d "%~dp0"
call just start

goto :end

:install_failed
echo.
echo [ERROR] Failed to install just
echo.
echo Please install manually from: https://github.com/casey/just
echo Then run: just start
echo.
pause
exit /b 1

:end

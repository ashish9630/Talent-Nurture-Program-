@echo off
echo Auto-updating Node.js...

:: Check if chocolatey is installed
choco --version >nul 2>&1
if %errorlevel% == 0 (
    echo Chocolatey found. Installing Node.js v20...
    choco install nodejs --version=20.19.0 -y
    goto :done
)

:: Check if winget is available
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo Winget found. Installing Node.js...
    winget install OpenJS.NodeJS --version 20.19.0
    goto :done
)

:: Manual download
echo Downloading Node.js v20.19.0...
powershell -Command "Invoke-WebRequest -Uri 'https://nodejs.org/dist/v20.19.0/node-v20.19.0-x64.msi' -OutFile 'nodejs-installer.msi'"
echo Installing Node.js...
msiexec /i nodejs-installer.msi /quiet
del nodejs-installer.msi

:done
echo Node.js installation complete!
echo Restarting command prompt...
pause
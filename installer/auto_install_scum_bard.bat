@echo off
setlocal EnableDelayedExpansion

:: Logging setup
set LOGFILE="%~dp0scum_bard_install.log"
echo [%date% %time%] Starting Scum Bard installation > %LOGFILE%

:: BatchGotAdmin
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges... >> %LOGFILE%
    powershell Start-Process '%0' -Verb RunAs
    exit /B
)

:: Comprehensive Dependency Checking
echo Checking system dependencies... >> %LOGFILE%

:: Python Check with Version Verification
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Attempting installation... >> %LOGFILE%
    powershell -Command "& {
        try {
            Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe' -OutFile 'python-installer.exe'
            Start-Process 'python-installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait
            Remove-Item 'python-installer.exe'
        } catch {
            Write-Error 'Failed to download Python'
        }
    }"
)

:: Verify Python installation and version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Critical: Python installation failed >> %LOGFILE%
    exit /B 1
)

:: Check for required software
where pip >nul 2>&1
if %errorlevel% neq 0 (
    python -m ensurepip --upgrade
)

:: Check for Inno Setup
where iscc >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Inno Setup...
    choco install innosetup -y
)

:: Create virtual environment
if not exist project_venv (
    python -m venv project_venv
    echo Virtual environment created >> %LOGFILE%
)

:: Activate virtual environment
call project_venv\Scripts\activate.bat

:: Upgrade pip and install dependencies with error handling
python -m pip install --upgrade pip
python -m pip install pyinstaller mido python-rtmidi pyautogui PyQt5
if %errorlevel% neq 0 (
    echo Dependency installation failed >> %LOGFILE%
    exit /B 1
)

:: Clean previous builds
if exist dist rmdir /s /q dist
mkdir dist

:: Navigate to Scum Bard plugin directory
cd plugins\scum_bard

:: Build executable
pyinstaller --onefile --windowed ^
    --add-data "..\..\scum-bard\data;data" ^
    --name scum_bard ^
    scum_bard.py

:: Check executable creation
if not exist ..\..\dist\scum_bard.exe (
    echo Executable creation failed >> %LOGFILE%
    exit /B 1
)

:: Move executable to project root
move dist\scum_bard.exe ..\..\dist\

:: Return to root directory
cd ..\..

:: Run Inno Setup Compiler
iscc setup.iss

:: Optional: Silently install the application
start /wait ScumBardInstaller.exe /SILENT

echo Installation completed successfully! >> %LOGFILE%
pause

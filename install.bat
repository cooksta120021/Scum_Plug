@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

REM Remove existing directory if it exists to prevent conflicts
if exist Scum_Plug (
    rmdir /s /q Scum_Plug
)

REM Clone the repository
git clone https://github.com/cooksta120021/Scum_Plug.git
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to clone repository.
    pause
    exit /b 1
)

REM Change to project directory
cd Scum_Plug

REM Create virtual environment
python -m venv project_venv
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
call project_venv\Scripts\activate
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo Installation completed successfully!
pause
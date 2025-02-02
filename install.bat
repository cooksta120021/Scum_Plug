@echo off
setlocal enabledelayedexpansion

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

:: Verify Python version
for /f "delims=" %%V in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%V"
echo Detected %PYTHON_VERSION%

:: Check Python version (basic check)
python -c "import sys; exit(0) if sys.version_info >= (3, 8) else exit(1)" 2>nul
if %errorlevel% neq 0 (
    echo Python 3.8+ is required. Current version is insufficient.
    pause
    exit /b 1
)

:: Create virtual environment
if not exist project_venv (
    echo Creating virtual environment...
    python -m venv project_venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install dependencies
call project_venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

:: Successful installation
echo Installation completed successfully!
pause
exit /b 0
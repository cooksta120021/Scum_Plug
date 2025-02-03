@echo off
setlocal enabledelayedexpansion

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

:: Activate virtual environment
call project_venv\Scripts\activate.bat

:: Navigate to Scum Bard plugin directory
cd plugins\scum_bard

:: Clean previous builds
if exist build rmdir /s /q build
if exist ..\..\dist rmdir /s /q ..\..\dist

:: Create executable
pyinstaller --onefile --windowed ^
    --add-data "..\..\scum-bard\data;data" ^
    --name scum_bard ^
    scum_bard.py

:: Check if PyInstaller succeeded
if not exist dist\scum_bard.exe (
    echo PyInstaller failed to create executable
    pause
    exit /b 1
)

:: Move executable to project root
move dist\scum_bard.exe ..\..\dist\

:: Return to root directory
cd ..\..

:: Check for Inno Setup
where iscc >nul 2>&1
if %errorlevel% neq 0 (
    echo Inno Setup compiler (iscc) not found. 
    echo Please install Inno Setup from https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

:: Build Windows installer
iscc setup.iss

echo Scum Bard build and installer creation completed successfully!
pause

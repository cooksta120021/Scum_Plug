# Change to project directory
Set-Location "Scum_Plug"

# Activate virtual environment
.\project_venv\Scripts\Activate.ps1

# Start the application in background
Start-Process pythonw.exe -ArgumentList "main.py"

Write-Host "Application started successfully" -ForegroundColor Green

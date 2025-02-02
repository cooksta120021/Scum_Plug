# Change to project directory
Set-Location "Scum_Plug"

# Deactivate virtual environment if active
if (Test-Path env:VIRTUAL_ENV) {
    deactivate
}

# Stop all Python processes related to the project
Stop-Process -Name "pythonw" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue

# Additional cleanup to ensure no lingering processes
Get-Process | Where-Object { $_.Path -like "*Scum_Plug*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "All Scum_Plug processes stopped and virtual environment deactivated." -ForegroundColor Yellow

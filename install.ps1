# Self-Elevating Installation Script for Scum_Plug

# Ensure we can run scripts and elevate privileges
try {
    # Try to set execution policy silently
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force -ErrorAction SilentlyContinue
} catch {}

# Ensure script runs with administrator privileges
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -Command `"& {$PSCommandPath}`"" -Verb RunAs
    exit
}

# Strict error handling and logging
$ErrorActionPreference = 'Stop'
$global:LogFile = "$PSScriptRoot\install_log.txt"

# Logging function
function Write-Log {
    param(
        [Parameter(Mandatory=$true)][string]$Message,
        [Parameter(Mandatory=$false)][string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Add-Content -Path $global:LogFile -Value $logMessage
    
    # Color coding for console output
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage }
    }
}

# Prerequisite check and installation function
function Install-Prerequisite {
    param(
        [string]$Name,
        [scriptblock]$CheckCommand,
        [scriptblock]$InstallCommand,
        [string[]]$ManualInstallInstructions
    )

    try {
        & $CheckCommand
        Write-Log "$Name is already installed." -Level "SUCCESS"
        return $true
    } catch {
        Write-Log "$Name is not installed. Attempting to install..." -Level "WARNING"
        
        # Comprehensive installation attempts
        $installMethods = @(
            { & $InstallCommand },
            { winget install $Name -e --accept-package-agreements --accept-source-agreements },
            { choco install $Name -y }
        )

        foreach ($method in $installMethods) {
            try {
                & $method
                Write-Log "$Name installed successfully." -Level "SUCCESS"
                return $true
            } catch {
                Write-Log "Installation method failed: $($_.Exception.Message)" -Level "WARNING"
            }
        }

        # Fallback download and install
        Write-Log "Automatic installation failed. Attempting direct download..." -Level "WARNING"
        try {
            # Direct download and silent install for Git
            if ($Name -eq "Git") {
                $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.40.1.windows.1/Git-2.40.1-64-bit.exe"
                $gitInstallerPath = "$env:TEMP\git-installer.exe"
                Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
                Start-Process $gitInstallerPath -ArgumentList "/SILENT /SUPPRESSMSGBOXES /NORESTART /SP-" -Wait
            }
            
            # Direct download and silent install for Python
            if ($Name -like "*Python*") {
                $pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe"
                $pythonInstallerPath = "$env:TEMP\python-installer.exe"
                Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
                Start-Process $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1" -Wait
            }
            
            Write-Log "$Name installed via direct download." -Level "SUCCESS"
            return $true
        } catch {
            Write-Log "Direct download installation failed for $Name" -Level "ERROR"
            Write-Host "`nManual Installation Required for $($Name):" -ForegroundColor Yellow
            foreach ($instruction in $ManualInstallInstructions) {
                Write-Host "- $instruction" -ForegroundColor Cyan
            }
            
            $choice = Read-Host "Do you want to continue without $Name? (y/n)"
            if ($choice -ne 'y') {
                Write-Log "Installation aborted due to missing $Name" -Level "ERROR"
                exit 1
            }
            return $false
        }
    }
}

# Repository and project details
$repoUrl = "https://github.com/cooksta120021/Scum_Plug.git"
$projectName = "Scum_Plug"
$installPath = "$PSScriptRoot\$projectName"

# Comprehensive prerequisite checks
function Confirm-Prerequisites {
    Write-Log "Checking system prerequisites..." -Level "INFO"

    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -lt 10) {
        Write-Log "Unsupported Windows version. Requires Windows 10 or later." -Level "ERROR"
        exit 1
    }

    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Log "Outdated PowerShell version. Please update to PowerShell 5 or later." -Level "ERROR"
        exit 1
    }

    # Install Git
    Install-Prerequisite -Name "Git" `
        -CheckCommand { git --version } `
        -InstallCommand { 
            Start-Process "winget" -ArgumentList "install", "Git.Git", "-e", "--accept-package-agreements", "--accept-source-agreements" -Wait
        } `
        -ManualInstallInstructions @(
            "Download from: https://git-scm.com/download/win",
            "Run the installer and follow the installation wizard"
        )

    # Install Python
    Install-Prerequisite -Name "Python.Python.3.11" `
        -CheckCommand { python --version } `
        -InstallCommand { 
            Start-Process "winget" -ArgumentList "install", "Python.Python.3.11", "-e", "--accept-package-agreements", "--accept-source-agreements" -Wait
        } `
        -ManualInstallInstructions @(
            "Download from: https://www.python.org/downloads/windows/",
            "Run the installer, check 'Add Python to PATH'"
        )

    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Repository installation function
function Install-Repository {
    param([string]$Path, [string]$Url)

    try {
        # Ensure clean installation
        if (Test-Path $Path) {
            Remove-Item $Path -Recurse -Force
        }

        # Clone repository
        git clone $Url $Path
        
        # Change to project directory
        Set-Location $Path

        # Update log file path to be inside the project directory
        $global:LogFile = "$installPath\install_log.txt"

        # Create virtual environment
        python -m venv project_venv
        
        # Activate virtual environment and install dependencies
        .\project_venv\Scripts\Activate.ps1
        pip install --upgrade pip
        pip install -r requirements.txt

        Write-Log "Repository installed successfully" -Level "SUCCESS"
    } catch {
        Write-Log "Repository installation failed: $($_.Exception.Message)" -Level "ERROR"
        exit 1
    }
}

# Main installation script
try {
    # Clear previous log (will be done inside the project directory after it's created)
    
    Write-Log "Starting Scum_Plug installation..." -Level "INFO"

    # Confirm and install prerequisites
    Confirm-Prerequisites

    # Install repository
    Install-Repository -Path $installPath -Url $repoUrl

    # Clear any existing log file in the new project directory
    if (Test-Path $global:LogFile) { Remove-Item $global:LogFile }

    Write-Log "Installation completed successfully!" -Level "SUCCESS"
    Write-Host "`nInstallation log saved to: $global:LogFile" -ForegroundColor Green

    # Optional: Pause to allow reading the output
    Start-Sleep -Seconds 5
} catch {
    Write-Log "Unexpected error during installation: $($_.Exception.Message)" -Level "ERROR"
    exit 1
}

# Scum Bard Installer

## Installation Instructions

1. Run `auto_install_scum_bard.bat` as administrator
   - This will automatically:
     - Install Python (if not present)
     - Create virtual environment
     - Install dependencies
     - Build executable
     - Create Windows installer
     - Optionally install the application

2. Alternatively, use the generated installer:
   - `ScumBardInstaller.exe`
   - Supports silent installation with `/SILENT` flag

## Management Scripts

- `start.bat`: Start the application
- `stop.bat`: Stop the application

## Troubleshooting

- Ensure you have administrative privileges
- Check internet connection
- Verify Python 3.8+ is installed

# Scum Plug Installation Guide

## Prerequisites
- Windows 10 or later
- Python 3.8+ installed
- Git (optional, but recommended)

## Installation Steps

### 1. Download the Project
#### Option A: Git Clone
```bash
git clone https://github.com/cooksta120021/Scum_Plug.git
cd Scum_Plug
```

#### Option B: Manual Download
- Download the ZIP from GitHub
- Extract to your desired location

### 2. Set Up Virtual Environment
```batch
# Create virtual environment
python -m venv project_venv

# Activate virtual environment
project_venv\Scripts\activate
```

### 3. Install Dependencies
```batch
pip install -r requirements.txt
```

## Running the Project

### Start the Application
```batch
start.bat
```

### Stop the Application
```batch
stop.bat
```

## Troubleshooting

### Python Not Recognized
- Ensure Python is installed
- Add Python to system PATH
- Use full path: `C:\Python39\python.exe`

### Dependency Issues
- Ensure virtual environment is activated
- Reinstall dependencies:
  ```batch
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

## Development

### Plugin Structure
- Plugins located in `plugins/` directory
- Each plugin has its own folder

### Logging
- Logs stored in `logs/` directory
- Check for runtime information and errors

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
[Insert License Information]

## Contact
[Insert Contact Information]

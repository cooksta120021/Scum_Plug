# ScumPlug: Plugin Management System

## Overview
ScumPlug is a lightweight Python application using PyQt5 for dynamic plugin management. It provides a centralized interface for loading and managing plugins.

## Features
- Auto-discovers plugins in `plugins/`
- Toggle plugins on/off
- Persistent overlay window
- Logging and error tracking

## Current Plugins
1. **Scum Browser** – Web browsing with event handling

## In Progress
1. **Social Network** – Firebase-based authentication & Google Sign-In

## Tech Stack
- **Python 3.11**
- **GUI**: PyQt5
- **Database**: Firebase
- **Logging**: Built-in system

## Installation & Usage
```bash
git clone https://github.com/yourusername/scumplug.git
cd scumplug
pip install -r requirements.txt
python main.py
```
- Click plugin buttons to toggle on/off
- Use system tray to exit

## Development
- Add plugins to `plugins/`
- Implement `create_plugin()` returning `QWidget`
- Auto-detected and added to UI

## Firestore Integration (Planned)
- Centralized storage for settings & usage
- Plugin state management & caching
- Secure authentication & best practices

## Packaging with PyInstaller
```bash
pyinstaller --name="ScumPlug" --windowed \
            --add-data "plugins:plugins" --add-data ".env:.env" \
            --hidden-import=PyQt5.QtWidgets \
            --hidden-import=PyQt5.QtCore \
            --hidden-import=PyQt5.QtGui \
            main.py
```

## Contribution & License
- Open for contributions via Pull Requests
- [Specify your license]

## Contact
cooksta120021@gmail.com

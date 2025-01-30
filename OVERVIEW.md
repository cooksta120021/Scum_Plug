# Scum Plug: Multi-Plugin Desktop Application

## Project Overview
Scum Plug is a modular desktop application built with PyQt5, designed to provide a flexible plugin-based architecture for various functionalities.

## Key Components

### Plugin System
- Dynamic plugin loading mechanism
- Supports multiple independent plugins
- Centralized plugin management through `main.py`

### Current Plugins

#### 1. Scum Browser Plugin
- Web browsing functionality
- Lightweight browser interface
- Integrated logging system
- Custom event handling

#### 2. Social Network Plugin
- Firebase-based authentication
- Social networking features
- Google Sign-In integration
- Logging and error tracking

## Technical Architecture

### Core Technologies
- Python 3.11
- PyQt5 for GUI
- Firebase for authentication and data management
- Modular plugin design

### Plugin Structure
- Each plugin has a dedicated directory
- Separate implementation and interface files
- Consistent `create_plugin()` function for instantiation
- Comprehensive logging mechanisms

## Dependencies
- PyQt5
- python-dotenv
- firebase-admin
- google-auth libraries
- requests

## Development Principles
- Separation of concerns
- Dynamic import mechanisms
- Robust error handling
- Comprehensive logging

## Future Roadmap
- Expand plugin ecosystem
- Enhance authentication flows
- Improve cross-plugin interactions
- Add more social networking features

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Firebase configuration
4. Run the application: `python main.py`

## Logging
Detailed logs are maintained for each plugin in their respective `logs/` directories, aiding in debugging and tracking application behavior.

## Packaging and Distribution

### Creating an Executable with PyInstaller

#### Prerequisites
- Install dependencies: `pip install -r requirements.txt`

#### Build Executable
```bash
# Basic build command
pyinstaller --name="ScumPlug" \
            --windowed \
            --add-data "plugins:plugins" \
            --add-data ".env:.env" \
            --hidden-import=PyQt5.QtWidgets \
            --hidden-import=PyQt5.QtCore \
            --hidden-import=PyQt5.QtGui \
            main.py
```

#### Build Options
- `--name="ScumPlug"`: Sets the executable name
- `--windowed`: Prevents console window from appearing
- `--add-data "plugins:plugins"`: Includes all plugins
- `--add-data ".env:.env"`: Includes environment configuration
- `--hidden-import=...`: Ensures Qt libraries are bundled

#### Troubleshooting
- Verify all dependencies are installed
- Check that plugins are correctly discovered
- Test the executable thoroughly after packaging

#### Distribution
- Executable will be in the `dist/` directory
- Distribute the entire `dist/ScumPlug` folder or executable

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

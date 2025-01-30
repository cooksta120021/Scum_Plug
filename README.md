# ScumPlug: Modular Plugin Management System

## Project Overview

ScumPlug is a flexible, lightweight Python application that provides a dynamic plugin management system using PyQt5. It offers a centralized interface for loading, managing, and interacting with various plugins, with a focus on ease of use and extensibility.

## Key Features

### Dynamic Plugin Loading
- Automatically discovers and loads plugins from the `plugins/` directory
- Supports multiple plugins with a simple, intuitive interface
- Each plugin is represented by a button in the main ScumPlug overlay

### Plugin Management
- Easy plugin activation and deactivation
- Plugins can be individually toggled on and off
- Persistent overlay window for quick access to plugins

### Current Plugins
- **Scum Browser**: A lightweight web browser plugin
  - Navigate to websites using URL input
  - Resizable browser window
  - Logging for tracking browser usage

## Technical Details

### Technology Stack
- **Language**: Python
- **GUI Framework**: PyQt5
- **Plugin Architecture**: Dynamic module loading
- **Logging**: Built-in logging for tracking plugin interactions

### System Requirements
- Python 3.7+
- PyQt5
- PyQtWebEngine

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/scum-plug.git
cd scum-plug
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Usage

1. Launch the ScumPlug application
2. Click on plugin buttons to activate/deactivate plugins
3. Interact with individual plugin windows as needed
4. Use the system tray icon or close button to exit the application

## Development

### Adding New Plugins
1. Create a new directory in the `plugins/` folder
2. Implement a `create_plugin()` function that returns a QWidget
3. The plugin will be automatically discovered and added to the ScumPlug interface

## Future Roadmap
- Support for plugin configuration
- Enhanced plugin management features
- More built-in plugins

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Specify your license here]

## Contact
[Your contact information]
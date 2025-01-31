import os
import sys
import json
import requests
import webbrowser
import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QMenu, QMessageBox, QMainWindow, 
                             QSystemTrayIcon, QAction, QStyle, QLabel, QSizePolicy)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon

from .plugin_button import PluginButton
from .custom_title_bar import CustomTitleBar

# Current version of the application
CURRENT_VERSION = "0.1.0"
GITHUB_REPO = "cooksta120021/Scum_Plug"

# Plugins directory
PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')

# Configuration file for plugin button settings
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugin_config.json')

class ScumPlug(QMainWindow):  
    def __init__(self):
        super().__init__()
        
        # Load plugin configuration
        self.plugin_config = self.load_plugin_config()
        
        # Initialize plugin buttons list
        self.plugin_buttons = []
        
        # Set window properties
        self.setWindowTitle("ScumPlug")
        self.setGeometry(100, 100, 400, 200)
        
        # Set window flags to remove default title bar, keep it frameless, and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        main_layout.setSpacing(0)  # Remove spacing
        
        # Create custom title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Create plugin buttons layout
        self.plugin_layout = QHBoxLayout()
        self.plugin_layout.setSpacing(10)  # Space between buttons
        plugin_widget = QWidget()
        plugin_widget.setLayout(self.plugin_layout)
        main_layout.addWidget(plugin_widget)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
        # Enable resizing
        self.installEventFilter(self)
        
        # Dynamically load plugins
        self.update_plugin_buttons()
        
        # Show the window
        self.show()
        
        # Connect close event to quit application
        self.closeEvent = self.handle_close_event
        
        # Restore window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
    
    def load_plugin_config(self):
        """
        Load plugin configuration from JSON file.
        If file doesn't exist, create a default configuration.
        """
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration: all plugins enabled
            default_config = {
                plugin_dir: True 
                for plugin_dir in os.listdir(PLUGINS_DIR) 
                if os.path.isdir(os.path.join(PLUGINS_DIR, plugin_dir))
            }
            
            # Save default configuration
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            return default_config
    
    def is_plugin_enabled(self, plugin_name):
        """
        Check if a plugin is enabled in the configuration.
        """
        return self.plugin_config.get(plugin_name, False)
    
    def toggle_plugin_button(self, plugin_name):
        """
        Toggle a plugin's enabled/disabled state.
        """
        # Toggle the plugin's configuration
        self.plugin_config[plugin_name] = not self.plugin_config.get(plugin_name, False)
        
        # Save updated configuration
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.plugin_config, f, indent=4)
        
        # Dynamically update plugin buttons
        self.update_plugin_buttons()
    
    def update_plugin_buttons(self):
        """
        Dynamically update plugin buttons based on current configuration.
        """
        # Clear existing plugin buttons
        for i in reversed(range(self.plugin_layout.count())): 
            widget = self.plugin_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Clear the plugin buttons list
        self.plugin_buttons.clear()
        
        # Dynamically load plugins
        for plugin_dir in os.listdir(PLUGINS_DIR):
            plugin_path = os.path.join(PLUGINS_DIR, plugin_dir)
            
            # Ensure it's a directory
            if os.path.isdir(plugin_path):
                # Check if plugin is enabled in configuration
                if self.is_plugin_enabled(plugin_dir):
                    # Create plugin button
                    plugin_button = PluginButton(plugin_dir, self)
                    self.plugin_layout.addWidget(plugin_button)
                    
                    # Add to plugin buttons list
                    self.plugin_buttons.append(plugin_button)
    
    def show_context_menu(self, pos):
        # Create custom context menu for plugin button toggling
        context_menu = QMenu(self)
        
        # Add Check for Updates action
        update_action = context_menu.addAction("Check for Updates")
        update_action.triggered.connect(self.check_for_updates)
        
        # Add a separator
        context_menu.addSeparator()
        
        # Add Plugin Toggle submenu
        plugin_menu = context_menu.addMenu("Toggle Plugins")
        
        # Create actions for each plugin
        for plugin_dir in os.listdir(PLUGINS_DIR):
            if os.path.isdir(os.path.join(PLUGINS_DIR, plugin_dir)):
                plugin_action = QAction(plugin_dir, self)
                plugin_action.setCheckable(True)
                plugin_action.setChecked(self.is_plugin_enabled(plugin_dir))
                
                # Connect action to toggle plugin
                plugin_action.triggered.connect(
                    lambda checked, name=plugin_dir: self.toggle_plugin_button(name)
                )
                
                plugin_menu.addAction(plugin_action)
        
        # Add a separator
        context_menu.addSeparator()
        
        # Add Exit Application action
        exit_action = context_menu.addAction("Exit Application")
        exit_action.triggered.connect(QApplication.quit)
        
        # Show menu at global position
        context_menu.exec_(self.mapToGlobal(pos))
    
    def handle_close_event(self, event):
        # Quit the entire application when window is closed
        QApplication.quit()
    
    def load_plugins(self):
        # Path to plugins directory
        plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
        
        # Check if plugins directory exists and is not empty
        if os.path.exists(plugins_dir) and os.listdir(plugins_dir):
            # Create a button for each plugin folder
            for plugin_name in os.listdir(plugins_dir):
                plugin_path = os.path.join(plugins_dir, plugin_name)
                
                # Skip if not a directory
                if not os.path.isdir(plugin_path):
                    continue
                
                # Check if the plugin directory has any Python files
                plugin_files = [f for f in os.listdir(plugin_path) if f.endswith('.py') and f != '__init__.py']
                
                # Only create a button if there are Python files in the directory
                if plugin_files:
                    btn = PluginButton(plugin_name, self)
                    self.plugin_layout.addWidget(btn)
                    self.plugin_buttons.append(btn)
    
    def load_plugin(self, plugin_name, button):
        # Import the plugin
        create_plugin = self.import_plugin(plugin_name)
        
        # Check if plugin import was successful
        if create_plugin:
            try:
                # Create plugin widget
                plugin_widget = create_plugin.create_plugin(button)
                
                # Verify it's a QWidget
                if not isinstance(plugin_widget, QWidget):
                    QMessageBox.warning(None, "Plugin Error", 
                                        f"Plugin {plugin_name} did not return a valid widget")
                    return None
                
                # Ensure plugin widget stays on top and has no window controls
                plugin_widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | 
                                             Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                
                # Show the plugin widget
                plugin_widget.show()
                return plugin_widget
            except Exception as e:
                QMessageBox.critical(None, "Plugin Load Error", 
                                     f"Failed to load plugin {plugin_name}: {str(e)}")
                return None
        
        return None
    
    def import_plugin(self, plugin_name):
        """
        Dynamically import a plugin with comprehensive logging and error handling
        
        :param plugin_name: Name of the plugin directory
        :return: Imported plugin module
        """
        try:
            # Path to plugins directory
            plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')
            
            # Find the plugin directory
            plugin_dir = os.path.join(plugins_dir, plugin_name)
            
            # Validate plugin directory exists
            if not os.path.isdir(plugin_dir):
                QMessageBox.warning(None, "Plugin Error", f"Plugin directory not found: {plugin_name}")
                return None
            
            # List all Python files in the plugin directory
            plugin_files = [
                f for f in os.listdir(plugin_dir) 
                if f.endswith('.py') and f != '__init__.py'
            ]
            
            if not plugin_files:
                QMessageBox.warning(None, "Plugin Error", f"No plugin files found for {plugin_name}")
                return None
            
            # Take the first Python file
            plugin_file = plugin_files[0]
            full_path = os.path.join(plugin_dir, plugin_file)
            
            # Import the module using importlib
            spec = importlib.util.spec_from_file_location(plugin_name, full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Verify create_plugin function exists
            if not hasattr(module, 'create_plugin'):
                QMessageBox.warning(None, "Plugin Error", f"No create_plugin function found in {plugin_name}")
                return None
            
            return module
        
        except Exception as e:
            QMessageBox.critical(None, "Plugin Import Error", 
                                 f"Error importing plugin {plugin_name}: {str(e)}")
            return None

    def check_for_updates(self):
        try:
            # GitHub Releases API URL (public, no authentication)
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            
            # Set a user agent to comply with GitHub API requirements
            headers = {
                'User-Agent': 'ScumPlug-Update-Checker'
            }
            
            # Fetch latest release
            response = requests.get(url, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release['tag_name'].lstrip('v')
                
                # Compare versions
                if latest_version > CURRENT_VERSION:
                    # Prepare update message
                    message = f"New version available!\n\n" \
                              f"Current version: {CURRENT_VERSION}\n" \
                              f"Latest version: {latest_version}\n\n" \
                              f"Release Notes:\n{latest_release.get('body', 'No release notes available')}\n\n" \
                              f"Would you like to download the update?"
                    
                    # Show update dialog
                    reply = QMessageBox.question(
                        None, 
                        "Update Available", 
                        message, 
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    # Open release page if user wants to update
                    if reply == QMessageBox.Yes:
                        webbrowser.open(latest_release['html_url'])
                else:
                    # Show up-to-date message
                    QMessageBox.information(
                        None, 
                        "No Updates Available", 
                        f"You are running the latest version ({CURRENT_VERSION})."
                    )
            else:
                # Handle API request failure
                QMessageBox.warning(
                    None, 
                    "Update Check Failed", 
                    f"Could not check for updates. Status code: {response.status_code}\n"
                    "Please check your internet connection."
                )
        except requests.RequestException as e:
            # Handle network-related errors
            QMessageBox.warning(
                None, 
                "Network Error", 
                f"A network error occurred:\n{str(e)}\n"
                "Please check your internet connection."
            )
        except Exception as e:
            # Handle any unexpected errors
            QMessageBox.critical(
                None, 
                "Update Error", 
                f"An unexpected error occurred:\n{str(e)}"
            )

    def save_window_state(self):
        """Save the window's position, size, and other persistent settings."""
        state = {
            'geometry': {
                'x': self.pos().x(),
                'y': self.pos().y(),
                'width': self.width(),
                'height': self.height()
            }
        }
        
        # Ensure config directory exists
        config_dir = os.path.join(os.path.expanduser('~'), '.scumplug')
        os.makedirs(config_dir, exist_ok=True)
        
        # Save state to a JSON file
        config_path = os.path.join(config_dir, 'window_state.json')
        with open(config_path, 'w') as f:
            json.dump(state, f)
    
    def restore_window_state(self):
        """Restore the window's previous position and size."""
        config_dir = os.path.join(os.path.expanduser('~'), '.scumplug')
        config_path = os.path.join(config_dir, 'window_state.json')
        
        try:
            with open(config_path, 'r') as f:
                state = json.load(f)
            
            # Restore geometry
            geo = state.get('geometry', {})
            x = geo.get('x', 100)
            y = geo.get('y', 100)
            width = geo.get('width', 400)
            height = geo.get('height', 200)
            
            self.setGeometry(x, y, width, height)
        except (FileNotFoundError, json.JSONDecodeError):
            # If no saved state, use default geometry
            self.setGeometry(100, 100, 400, 200)

    def eventFilter(self, obj, event):
        # Handle window resizing
        if obj == self and event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                # Get mouse position relative to window
                pos = event.pos()
                
                # Define resize margins
                margin = 10
                
                # Check if mouse is near bottom-right corner
                if (pos.x() >= self.width() - margin and 
                    pos.y() >= self.height() - margin):
                    # Start resize
                    self.start_resize = True
                    self.resize_start_pos = event.globalPos()
                    return True
        
        elif obj == self and event.type() == QEvent.MouseMove:
            if hasattr(self, 'start_resize') and self.start_resize:
                # Calculate new size
                current_pos = event.globalPos()
                diff = current_pos - self.resize_start_pos
                
                # Resize window
                new_width = max(65, self.width() + diff.x())
                new_height = max(25, self.height() + diff.y())
                
                self.resize(new_width, new_height)
                
                # Update start position
                self.resize_start_pos = current_pos
                return True
        
        elif obj == self and event.type() == QEvent.MouseButtonRelease:
            if hasattr(self, 'start_resize'):
                # End resize
                del self.start_resize
                return True
        
        return super().eventFilter(obj, event)

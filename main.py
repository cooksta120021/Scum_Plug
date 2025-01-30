import os
import sys
import traceback
import logging
import importlib.util

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'application_startup.log')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a logger for startup
logger = logging.getLogger('ApplicationStartup')

# Capture any startup errors
try:
    # Log system and environment information
    logger.info("Application Startup Initiated")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Python Executable: {sys.executable}")
    logger.info(f"Current Working Directory: {os.getcwd()}")
    logger.info(f"Python Path: {sys.path}")

    # Original imports and code continue here
    import warnings
    warnings.filterwarnings("ignore")

    import os
    import sys
    import traceback
    import requests
    import webbrowser
    from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                                 QPushButton, QMenu, QInputDialog, QMessageBox,
                                 QSystemTrayIcon, QAction, QMainWindow, QStyle, QLabel, 
                                 QSizePolicy)
    from PyQt5.QtCore import Qt, QMimeData, QPoint, QEvent
    from PyQt5.QtGui import QIcon, QDrag

    # Current version of the application
    CURRENT_VERSION = "0.1.0"
    GITHUB_REPO = "cooksta120021/Scum_Plug"

    # Set OpenGL context sharing before creating QApplication
    import PyQt5.QtCore
    PyQt5.QtCore.QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    import os
    import sys
    import importlib.util
    import traceback
    import logging

    # Set up logging
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'plugin_import.log')

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Create a logger for this module
    logger = logging.getLogger('PluginImporter')

    # Plugins directory
    PLUGINS_DIR = os.path.join(os.path.dirname(__file__), 'plugins')

    def import_plugin(plugin_name):
        """
        Dynamically import a plugin with comprehensive logging and error handling
        
        :param plugin_name: Name of the plugin directory
        :return: Imported plugin module
        """
        try:
            # Log the start of plugin import
            logger.info(f"Attempting to import plugin: {plugin_name}")
            logger.info(f"Plugin path: {os.path.join(PLUGINS_DIR, plugin_name)}")
            
            # Log current Python path
            logger.info("Current Python path:")
            for path in sys.path:
                logger.info(f"  - {path}")
            
            # Find the plugin directory
            plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
            
            # Validate plugin directory exists
            if not os.path.isdir(plugin_dir):
                logger.error(f"Plugin directory not found: {plugin_dir}")
                raise ImportError(f"Plugin directory not found: {plugin_name}")
            
            # List all Python files in the plugin directory
            plugin_files = [
                f for f in os.listdir(plugin_dir) 
                if f.endswith('.py') and f != '__init__.py'
            ]
            
            # Log found plugin files
            logger.info(f"Plugin files found: {plugin_files}")
            
            if not plugin_files:
                logger.error(f"No plugin files found in {plugin_dir}")
                raise ImportError(f"No plugin files found for {plugin_name}")
            
            # Take the first Python file
            plugin_file = plugin_files[0]
            full_path = os.path.join(plugin_dir, plugin_file)
            
            # Log the specific file being imported
            logger.info(f"Importing plugin file: {full_path}")
            
            # Add the plugin directory to Python path
            sys.path.insert(0, plugin_dir)
            
            # Import the module using importlib
            spec = importlib.util.spec_from_file_location(plugin_name, full_path)
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Log successful module import
            logger.info(f"Successfully imported plugin module: {module}")
            logger.info(f"Module attributes: {dir(module)}")
            
            return module
        
        except Exception as e:
            # Comprehensive error logging
            logger.error(f"Error importing plugin {plugin_name}: {e}")
            logger.error(traceback.format_exc())
            
            # Reraise the exception
            raise

    class PluginButton(QPushButton):
        def __init__(self, plugin_name, overlay):
            super().__init__(plugin_name)
            
            # Store plugin information
            self.plugin_name = plugin_name
            self.overlay = overlay
            self.active_plugin = None
            
            # Disable dragging
            self.setMouseTracking(False)
            
            # Make button non-movable and resize with parent
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            # Button styling
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 100, 200, 230);
                    color: white;
                    border: 3px solid white;
                    border-radius: 15px;
                    font-weight: bold;
                    font-size: 14px;
                    text-transform: uppercase;
                }
                QPushButton:hover {
                    background-color: rgba(70, 120, 220, 250);
                }
            """)
            
            # Context menu for button
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menu)
        
        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                # If not dragging, toggle plugin
                if not self.active_plugin:
                    self.active_plugin = self.overlay.load_plugin(self.plugin_name, self)
                    
                    # Change button style when plugin is loaded
                    if self.active_plugin:
                        self.setStyleSheet("""
                            QPushButton {
                                background-color: rgba(0, 255, 0, 230);
                                color: white;
                                border: 3px solid white;
                                border-radius: 15px;
                                font-weight: bold;
                                font-size: 14px;
                                text-transform: uppercase;
                            }
                        """)
                else:
                    # Toggle visibility of active plugin
                    if self.active_plugin.isVisible():
                        self.active_plugin.hide()
                        self.setStyleSheet("""
                            QPushButton {
                                background-color: rgba(50, 100, 200, 230);
                                color: white;
                                border: 3px solid white;
                                border-radius: 15px;
                                font-weight: bold;
                                font-size: 14px;
                                text-transform: uppercase;
                            }
                        """)
                    else:
                        self.active_plugin.show()
                        self.setStyleSheet("""
                            QPushButton {
                                background-color: rgba(0, 255, 0, 230);
                                color: white;
                                border: 3px solid white;
                                border-radius: 15px;
                                font-weight: bold;
                                font-size: 14px;
                                text-transform: uppercase;
                            }
                        """)
            
            super().mousePressEvent(event)
        
        def show_context_menu(self, pos):
            # Create context menu
            context_menu = QMenu(self)
            
            # Add Check for Updates action
            update_action = context_menu.addAction("Check for Updates")
            update_action.triggered.connect(self.overlay.check_for_updates)
            
            # Add Exit Application action
            exit_action = context_menu.addAction("Exit Application")
            exit_action.triggered.connect(QApplication.quit)
            
            # Show menu at global position
            context_menu.exec_(self.mapToGlobal(pos))
        
        def exit_plugin(self):
            # Close and destroy the active plugin if exists
            if self.active_plugin:
                self.active_plugin.close()
                self.active_plugin.deleteLater()  # Ensure complete destruction
                self.active_plugin = None
                
                # Reset button style
                self.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(50, 100, 200, 230);
                        color: white;
                        border: 3px solid white;
                        border-radius: 15px;
                        font-weight: bold;
                        font-size: 14px;
                        text-transform: uppercase;
                    }
                """)

    class CustomTitleBar(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            
            # Create layout
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Create title label
            self.title_label = QLabel("ScumPlug Overlay")
            self.title_label.setAlignment(Qt.AlignCenter)
            self.title_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: black;
                    font-weight: bold;
                }
            """)
            
            # Add title label to layout
            layout.addWidget(self.title_label)
            
            # Set layout
            self.setLayout(layout)
            
            # Enable custom context menu
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.show_context_menu)
            
            # Make widget draggable
            self.mousePressEvent = self.mouse_press
            self.mouseMoveEvent = self.mouse_move
        
        def mouse_press(self, event):
            if event.button() == Qt.LeftButton:
                # Store the current mouse position
                self.drag_start_position = event.globalPos()
                # Get the parent window
                self.parent_window = self.parent().parent()
        
        def mouse_move(self, event):
            if event.buttons() == Qt.LeftButton:
                # Calculate the distance moved
                current_pos = event.globalPos()
                diff = current_pos - self.drag_start_position
                
                # Move the parent window
                new_pos = self.parent_window.pos() + diff
                self.parent_window.move(new_pos)
                
                # Update the start position
                self.drag_start_position = current_pos
        
        def show_context_menu(self, pos):
            # Create custom context menu for title bar
            context_menu = QMenu(self)
            
            # Add Check for Updates action
            update_action = context_menu.addAction("Check for Updates")
            update_action.triggered.connect(self.parent().parent().check_for_updates)
            
            # Add Exit Application action
            exit_action = context_menu.addAction("Exit Application")
            exit_action.triggered.connect(QApplication.quit)
            
            # Show menu at global position
            context_menu.exec_(self.mapToGlobal(pos))

    class ScumPlug(QMainWindow):  # Changed to QMainWindow for taskbar visibility
        def __init__(self):
            super().__init__()
            
            # Ensure QApplication exists
            self.app = QApplication.instance()
            if not self.app:
                self.app = QApplication(sys.argv)
            
            # Remove default window title
            self.setWindowTitle("")
            
            # Set window flags to remove default title bar and keep it frameless
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
            
            # Create central widget and main layout
            central_widget = QWidget()
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
            main_layout.setSpacing(0)  # Remove spacing
            
            # Create title bar
            self.title_bar = CustomTitleBar(self)
            main_layout.addWidget(self.title_bar)  # Add title bar to top
            
            # Create plugin layout with expanding horizontal policy
            self.plugin_layout = QHBoxLayout()
            self.plugin_layout.setSpacing(10)  # Space between buttons
            plugin_widget = QWidget()
            plugin_widget.setLayout(self.plugin_layout)
            main_layout.addWidget(plugin_widget)
            
            # Set central widget
            self.setCentralWidget(central_widget)
            
            # Set default size to match plugin window
            self.setGeometry(100, 100, 400, 200)
            
            # Enable resizing
            self.installEventFilter(self)
            
            # Load plugins
            self.load_plugins()
            
            # Show the window
            self.show()
            
            # Connect close event to quit application
            self.closeEvent = self.handle_close_event
        
        def handle_close_event(self, event):
            # Quit the entire application when window is closed
            QApplication.quit()
        
        def load_plugins(self):
            # Path to plugins directory
            plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
            
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
        
        def load_plugin(self, plugin_name, button):
            # Import the plugin
            create_plugin = import_plugin(plugin_name)
            
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

    def main():
        # Ensure QApplication is created
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        
        # Create the main window
        main_window = ScumPlug()
        
        # Create system tray icon
        tray_icon = QSystemTrayIcon()
        # Use a default system icon
        tray_icon.setIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Create tray menu
        tray_menu = QMenu()
        exit_action = QAction("Exit", tray_menu)
        exit_action.triggered.connect(app.quit)
        tray_menu.addAction(exit_action)
        
        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()
        
        # Start event loop
        sys.exit(app.exec_())

    # Ensure requests is installed
    try:
        import requests
    except ImportError:
        print("Installing required dependencies...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        import requests

    if __name__ == '__main__':
        main()

except Exception as startup_error:
    # Catch and log any startup errors
    logger.critical("Fatal error during application startup")
    logger.critical(traceback.format_exc())
    
    # Optional: Show error message box
    try:
        app = QApplication(sys.argv)
        QMessageBox.critical(
            None, 
            "Startup Error", 
            f"A critical error occurred during startup:\n{startup_error}\n\n"
            "Please check the log file for more details."
        )
    except Exception as msg_error:
        logger.critical(f"Could not display error message: {msg_error}")
    
    # Exit with error code
    sys.exit(1)

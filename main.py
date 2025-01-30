import os
import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QMenu, QInputDialog, QMessageBox,
                             QSystemTrayIcon, QAction, QMainWindow, QStyle, QLabel, 
                             QSizePolicy)
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QIcon, QDrag

# Set OpenGL context sharing before creating QApplication
import PyQt5.QtCore
PyQt5.QtCore.QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Dynamically import plugins
def import_plugin(plugin_name):
    try:
        # Construct full path to plugin directory
        plugin_path = os.path.join(os.path.dirname(__file__), 'plugins', plugin_name)
        
        # Add plugin directory to Python path
        sys.path.insert(0, plugin_path)
        
        # Log import details
        print(f"Attempting to import plugin: {plugin_name}")
        print(f"Plugin path: {plugin_path}")
        print(f"Current Python path: {sys.path}")
        
        # Try importing the module
        module = __import__('browser', fromlist=['create_plugin'])
        
        # Log successful import
        print(f"Successfully imported plugin module: {module}")
        print(f"Module attributes: {dir(module)}")
        
        # Return the create_plugin function
        return module.create_plugin
    except Exception as e:
        # Detailed error logging
        print(f"Error importing plugin {plugin_name}: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

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
        context_menu = QMenu(self)
        
        # Exit plugin action
        exit_action = context_menu.addAction("Exit Plugin")
        exit_action.triggered.connect(self.exit_plugin)
        
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

class ScumPlug(QMainWindow):  # Changed to QMainWindow for taskbar visibility
    def __init__(self):
        super().__init__()
        
        # Ensure QApplication exists
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        # Configure main window
        self.setWindowTitle("ScumPlug Overlay")
        self.setGeometry(100, 100, 400, 150)  # Wider initial size
        
        # Ensure window stays on top and has standard window controls
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | 
                            Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add some padding
        main_layout.setSpacing(10)  # Add spacing between elements
        
        # Create plugin layout with expanding horizontal policy
        self.plugin_layout = QHBoxLayout()
        self.plugin_layout.setSpacing(10)  # Space between buttons
        main_layout.addLayout(self.plugin_layout)
        
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
                plugin_widget = create_plugin(button)
                
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

if __name__ == '__main__':
    main()

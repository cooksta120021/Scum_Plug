import sys
import traceback
import logging
import os

# Explicitly use PyQt5 imports
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                             QMessageBox, QApplication)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'browser_plugin.log')
logging.basicConfig(
    filename=log_file, 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ScumBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        try:
            logging.info("Initializing ScumBrowserWidget")
            
            # Create layout
            layout = QVBoxLayout()
            
            # Create URL input
            self.url_input = QLineEdit(self)
            self.url_input.setPlaceholderText("Enter URL and press Enter")
            self.url_input.returnPressed.connect(self.navigate)
            layout.addWidget(self.url_input)
            
            # Create web view
            self.web_view = QWebEngineView(self)
            layout.addWidget(self.web_view)
            
            # Set layout
            self.setLayout(layout)
            
            # Set initial size
            self.resize(800, 600)
            
            # Set window title
            self.setWindowTitle("Scum Browser")
            
            logging.info("ScumBrowserWidget initialized successfully")
        
        except Exception as e:
            logging.error(f"Fatal error in ScumBrowserWidget initialization: {e}")
            logging.error(traceback.format_exc())
            QMessageBox.critical(None, "Browser Initialization Error", 
                                 f"Failed to initialize browser:\n{e}\n\n"
                                 f"Check log at {log_file} for details")
            raise
    
    def navigate(self):
        try:
            url = self.url_input.text()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            logging.info(f"Navigating to URL: {url}")
            self.web_view.setUrl(QUrl(url))
        except Exception as e:
            logging.error(f"Error navigating to URL: {e}")
            QMessageBox.warning(self, "Navigation Error", f"Failed to navigate: {e}")

def create_plugin(button=None):
    # Ensure QApplication exists
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Create widget
    widget = ScumBrowserWidget()
    
    # Explicitly log and verify widget type
    logging.info(f"Created plugin widget: {type(widget)}")
    
    # Ensure it's a QWidget
    if not isinstance(widget, QWidget):
        logging.error("Created object is not a QWidget!")
        raise TypeError("Plugin must return a QWidget instance")
    
    return widget

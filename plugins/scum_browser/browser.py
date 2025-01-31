import sys
import traceback
import logging
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                             QMessageBox, QApplication, QShortcut)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PyQt5.QtGui import QKeySequence
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

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Suppress specific non-critical warnings
        suppressed_warnings = [
            "A cookie associated with a cross-site resource",
            "was preloaded using link preload but not used",
            "A future release of Chrome will only deliver cookies"
        ]
        
        # Check if the message contains any of the suppressed warnings
        if not any(warning in message for warning in suppressed_warnings):
            # Log only non-suppressed messages
            logging.info(f"JS Console: {message}")

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
            
            # Create web view with custom page
            self.web_view = QWebEngineView(self)
            custom_page = CustomWebEnginePage(self.web_view)
            self.web_view.setPage(custom_page)
            
            # Disable JavaScript warnings and non-critical console messages
            settings = self.web_view.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
            
            layout.addWidget(self.web_view)
            
            # Set layout
            self.setLayout(layout)
            
            # Set initial size
            self.resize(800, 600)
            
            # Set window title
            self.setWindowTitle("Scum Browser")
            
            # Set initial zoom level
            self.current_zoom = 1.0
            
            # Add zoom shortcuts
            self.setup_zoom_shortcuts()
            
            logging.info("ScumBrowserWidget initialized successfully")
        
        except Exception as e:
            logging.error(f"Fatal error in ScumBrowserWidget initialization: {e}")
            logging.error(traceback.format_exc())
            QMessageBox.critical(None, "Browser Initialization Error", 
                                 f"Failed to initialize browser:\n{e}\n\n"
                                 f"Check log at {log_file} for details")
            raise
    
    def setup_zoom_shortcuts(self):
        # Zoom in shortcut (Ctrl + +)
        zoom_in_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Equal), self)
        zoom_in_shortcut.activated.connect(self.zoom_in)
        
        # Zoom out shortcut (Ctrl + -)
        zoom_out_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus), self)
        zoom_out_shortcut.activated.connect(self.zoom_out)
        
        # Reset zoom shortcut (Ctrl + 0)
        reset_zoom_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_0), self)
        reset_zoom_shortcut.activated.connect(self.reset_zoom)
    
    def zoom_in(self):
        self.current_zoom = min(5.0, self.current_zoom + 0.1)
        self.web_view.setZoomFactor(self.current_zoom)
        logging.info(f"Zoomed in. Current zoom: {self.current_zoom:.1f}")
    
    def zoom_out(self):
        self.current_zoom = max(0.1, self.current_zoom - 0.1)
        self.web_view.setZoomFactor(self.current_zoom)
        logging.info(f"Zoomed out. Current zoom: {self.current_zoom:.1f}")
    
    def reset_zoom(self):
        self.current_zoom = 1.0
        self.web_view.setZoomFactor(self.current_zoom)
        logging.info("Zoom reset to default")
    
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

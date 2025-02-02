import sys
import traceback
import logging
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                             QMessageBox, QApplication, QShortcut, QHBoxLayout, 
                             QPushButton, QSlider, QMenu, QAction, QLabel)
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
    DEFAULT_SEARCH_ENGINE = "https://www.google.com/search?q="
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        try:
            logging.info("Initializing ScumBrowserWidget")
            
            # Create main layout
            main_layout = QVBoxLayout()
            
            # Create navigation layout
            nav_layout = QHBoxLayout()
            
            # Create back button
            self.back_button = QPushButton("←", self)
            self.back_button.clicked.connect(self.go_back)
            nav_layout.addWidget(self.back_button)
            
            # Create forward button
            self.forward_button = QPushButton("→", self)
            self.forward_button.clicked.connect(self.go_forward)
            nav_layout.addWidget(self.forward_button)
            
            # Create URL input
            self.url_input = QLineEdit(self)
            self.url_input.setPlaceholderText("Enter URL or search term")
            self.url_input.returnPressed.connect(self.navigate)
            nav_layout.addWidget(self.url_input)
            
            # Add navigation layout to main layout
            main_layout.addLayout(nav_layout)
            
            # Create web view with custom page
            self.web_view = QWebEngineView(self)
            custom_page = CustomWebEnginePage(self.web_view)
            self.web_view.setPage(custom_page)
            
            # Disable JavaScript warnings and non-critical console messages
            settings = self.web_view.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
            
            main_layout.addWidget(self.web_view)
            
            # Create transparency slider
            transparency_layout = QHBoxLayout()
            transparency_label = QLabel("Transparency:")
            self.transparency_slider = QSlider(Qt.Horizontal)
            self.transparency_slider.setMinimum(10)  # Minimum 10% opacity
            self.transparency_slider.setMaximum(100)  # Maximum 100% opacity
            self.transparency_slider.setValue(100)  # Default to fully opaque
            self.transparency_slider.valueChanged.connect(self.adjust_transparency)
            
            transparency_layout.addWidget(transparency_label)
            transparency_layout.addWidget(self.transparency_slider)
            main_layout.addLayout(transparency_layout)
            
            # Set layout
            self.setLayout(main_layout)
            
            # Set initial size
            self.resize(800, 600)
            
            # Set window title
            self.setWindowTitle("Scum Browser")
            
            # Set initial zoom level
            self.current_zoom = 1.0
            
            # Add zoom shortcuts
            self.setup_zoom_shortcuts()
            
            # Setup context menu
            self.setup_context_menu()
            
            # Set default homepage
            self.navigate_to_homepage()
            
            logging.info("ScumBrowserWidget initialized successfully")
        
        except Exception as e:
            logging.error(f"Fatal error in ScumBrowserWidget initialization: {e}")
            logging.error(traceback.format_exc())
            QMessageBox.critical(None, "Browser Initialization Error", 
                                 f"Failed to initialize browser:\n{e}\n\n"
                                 f"Check log at {log_file} for details")
            raise
    
    def go_back(self):
        """Navigate to the previous page in browsing history."""
        if self.web_view.history().canGoBack():
            self.web_view.history().back()
            logging.info("Navigated back in browsing history")
    
    def go_forward(self):
        """Navigate to the next page in browsing history."""
        if self.web_view.history().canGoForward():
            self.web_view.history().forward()
            logging.info("Navigated forward in browsing history")
    
    def toggle_javascript(self):
        """Toggle JavaScript on/off for the current page."""
        settings = self.web_view.settings()
        current_js_state = settings.getAttribute(QWebEngineSettings.JavascriptEnabled)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, not current_js_state)
        logging.info(f"JavaScript {'disabled' if current_js_state else 'enabled'}")
        
        # Reload the page to apply changes
        self.web_view.reload()
        
        return not current_js_state
    
    def navigate_to_homepage(self):
        """Navigate to the default homepage (Google)."""
        homepage = "https://www.google.com"
        logging.info(f"Navigating to homepage: {homepage}")
        self.web_view.setUrl(QUrl(homepage))
        self.url_input.setText(homepage)
    
    def navigate(self):
        try:
            input_text = self.url_input.text().strip()
            if not input_text:
                logging.warning("Empty input entered")
                QMessageBox.warning(self, "Invalid Input", "Please enter a URL or search term")
                return
            
            # Check if input is a search term
            if ' ' in input_text or not input_text.startswith(('http://', 'https://', 'www.')):
                # Treat as search query
                search_url = f"{self.DEFAULT_SEARCH_ENGINE}{input_text.replace(' ', '+')}"
                logging.info(f"Performing Google search for: {input_text}")
                url = QUrl(search_url)
            else:
                # Ensure protocol is present
                url = QUrl(input_text if input_text.startswith(('http://', 'https://')) else 'https://' + input_text)
            
            # Validate URL
            if not url.isValid():
                raise ValueError(f"Invalid URL or search query: {input_text}")
            
            self.web_view.setUrl(url)
            self.url_input.setText(url.toString())  # Update input with full URL
            logging.info(f"Navigated to: {url.toString()}")
        
        except Exception as e:
            logging.error(f"Error navigating/searching: {e}")
            error_msg = f"Failed to navigate/search for: {input_text}\nError: {str(e)}"
            QMessageBox.warning(self, "Navigation Error", error_msg)
    
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
    
    def setup_context_menu(self):
        """Set up context menu for additional browser controls."""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos):
        """Display context menu with transparency options."""
        context_menu = QMenu(self)
        
        # Transparency submenu
        transparency_menu = context_menu.addMenu("Transparency")
        
        # Predefined transparency levels
        transparency_levels = [
            ("100%", 100),
            ("90%", 90),
            ("80%", 80),
            ("70%", 70),
            ("60%", 60),
            ("50%", 50)
        ]
        
        for label, value in transparency_levels:
            action = transparency_menu.addAction(label)
            action.triggered.connect(lambda checked, v=value: self.set_transparency(v))
        
        # JavaScript toggle
        js_toggle = context_menu.addAction("Toggle JavaScript")
        js_toggle.triggered.connect(self.toggle_javascript)
        
        context_menu.exec_(self.mapToGlobal(pos))
    
    def adjust_transparency(self, value):
        """Adjust window transparency based on slider value."""
        # Convert percentage to opacity (0.0 to 1.0)
        opacity = value / 100.0
        self.setWindowOpacity(opacity)
        logging.info(f"Window transparency set to {value}%")
    
    def set_transparency(self, value):
        """Set transparency to a specific value."""
        self.transparency_slider.setValue(value)
        self.adjust_transparency(value)

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

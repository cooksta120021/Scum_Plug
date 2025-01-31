import sys
import traceback
import logging
import os
from dotenv import load_dotenv

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'social_network.log')

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
logger = logging.getLogger('SocialNetworkPlugin')

# Log the start of the module
logger.info("Social Network Plugin module initialized")
logger.info(f"Log file created at: {log_file}")

# Add the parent directory to Python path to enable imports
plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, plugin_dir)

from social_network_impl.firebase_config import create_collections, initialize_firebase, google_sign_in

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QMessageBox, QApplication, QPushButton, 
                             QLabel, QScrollArea, QTextEdit, 
                             QDialog, QMainWindow)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import Firebase configuration
# from .firebase_config import create_collections, initialize_firebase, google_sign_in

class ScumPlugOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Make the overlay transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        
        # Scum Plug logo or text
        self.logo_label = QLabel("Scum Plug")
        self.logo_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);
            color: white;
            padding: 10px;
            border-radius: 10px;
        """)
        layout.addWidget(self.logo_label)
        
        self.setLayout(layout)
        
        # Position overlay
        self.resize(200, 100)
        self.move(10, 10)  # Top-left corner

class SocialNetworkWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        try:
            logger.info("Initializing SocialNetworkWidget")
            
            # Create layout
            layout = QVBoxLayout()
            
            # Login Section
            login_layout = QVBoxLayout()
            
            # Google Sign-In Button
            self.google_login_button = QPushButton("Sign in with Google")
            self.google_login_button.clicked.connect(self.google_sign_in)
            login_layout.addWidget(self.google_login_button)
            
            # User Info Label
            self.user_info_label = QLabel("Not Signed In")
            login_layout.addWidget(self.user_info_label)
            
            layout.addLayout(login_layout)
            
            # Post Creation Section
            post_layout = QHBoxLayout()
            self.post_input = QTextEdit()
            self.post_input.setPlaceholderText("What's on your mind?")
            self.post_input.setMaximumHeight(100)
            
            self.post_button = QPushButton("Post")
            self.post_button.clicked.connect(self.create_post)
            self.post_button.setEnabled(False)  # Disable until signed in
            
            post_layout.addWidget(self.post_input)
            post_layout.addWidget(self.post_button)
            layout.addLayout(post_layout)
            
            # Posts Display Section
            self.posts_scroll = QScrollArea()
            self.posts_widget = QWidget()
            self.posts_layout = QVBoxLayout(self.posts_widget)
            self.posts_scroll.setWidget(self.posts_widget)
            self.posts_scroll.setWidgetResizable(True)
            
            layout.addWidget(self.posts_scroll)
            
            # Set layout
            self.setLayout(layout)
            
            # Set initial size
            self.resize(800, 600)
            
            # Set window title
            self.setWindowTitle("Social Network")
            
            logger.info("SocialNetworkWidget initialized successfully")
        
        except Exception as e:
            logger.error(f"Fatal error in SocialNetworkWidget initialization: {e}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Social Network Initialization Error", 
                                 f"Failed to initialize social network:\n{e}\n\n"
                                 f"Check log at {log_file} for details")
            raise
    
    def google_sign_in(self):
        try:
            # Call Google Sign-In from Firebase configuration
            sign_in_result = google_sign_in()
            
            if sign_in_result.get('success'):
                # Update UI to show user is signed in
                user = sign_in_result.get('user', {})
                self.user_info_label.setText(f"Signed in as: {user.get('displayName', 'User')}")
                
                # Enable post button
                self.post_button.setEnabled(True)
                
                # Show success message
                QMessageBox.information(self, "Google Sign-In", 
                                        sign_in_result.get('message', 'Signed in successfully'))
            else:
                # Show error message
                QMessageBox.warning(self, "Google Sign-In", 
                                    sign_in_result.get('message', 'Failed to sign in'))
        
        except Exception as e:
            logger.error(f"Google Sign-In error: {e}")
            QMessageBox.warning(self, "Google Sign-In Failed", str(e))
    
    def create_post(self):
        try:
            post_content = self.post_input.toPlainText()
            
            if not post_content:
                QMessageBox.warning(self, "Invalid Post", "Please enter post content.")
                return
            
            # Create post widget
            post_widget = QWidget()
            post_layout = QVBoxLayout(post_widget)
            
            content_label = QLabel(post_content)
            content_label.setWordWrap(True)
            
            post_layout.addWidget(content_label)
            
            # Add post to posts layout
            self.posts_layout.insertWidget(0, post_widget)
            
            # Clear input fields
            self.post_input.clear()
            
            logger.info("New post created")
        
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            QMessageBox.warning(self, "Post Error", f"Failed to create post: {e}")

def create_plugin(button=None):
    # Ensure QApplication exists
    from PyQt5.QtWidgets import QApplication, QWidget
    
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    
    # Create widget
    widget = SocialNetworkWidget()
    
    # Explicitly log and verify widget type
    logger.info(f"Created plugin widget: {type(widget)}")
    
    # Ensure it's a QWidget
    if not isinstance(widget, QWidget):
        logger.error("Created object is not a QWidget!")
        raise TypeError("Plugin must return a QWidget instance")
    
    return widget

def main():
    app = QApplication(sys.argv)
    
    # Initialize Firebase configuration
    initialize_firebase()
    
    # Initialize collections (placeholder)
    create_collections()
    
    # Create social network widget
    social_network = SocialNetworkWidget()
    social_network.show()
    
    # Create ScumPlug overlay
    overlay = ScumPlugOverlay()
    overlay.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

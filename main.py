import os
import sys
import traceback
import logging
import importlib.util
import json
import PyQt5.QtCore
from PyQt5.QtCore import Qt

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'application_startup.log')

# Set OpenGL context sharing before creating QApplication
PyQt5.QtCore.QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

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

    import warnings
    warnings.filterwarnings("ignore")

    import requests
    import webbrowser
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QStyle
    from core import ScumPlug

    # Ensure requests is installed
    try:
        import requests
    except ImportError:
        print("Installing required dependencies...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        import requests

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

except Exception as startup_error:
    # Catch and log any startup errors
    logger.critical("Fatal error during application startup")
    logger.critical(traceback.format_exc())
    
    # Optional: Show error message box
    try:
        app = QApplication(sys.argv)
        from PyQt5.QtWidgets import QMessageBox
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

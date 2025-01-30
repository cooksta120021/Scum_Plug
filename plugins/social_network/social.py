import os
import sys
import importlib.util
import traceback
import logging

# Add the plugin directory to Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_dir)
sys.path.insert(0, os.path.join(plugin_dir, 'social_network_impl'))

# Set up logging
log_dir = os.path.join(plugin_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'social_plugin_import.log')

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
logger = logging.getLogger('SocialPluginImport')

# Log the start of the module
logger.info("Social Plugin Import module initialized")
logger.info(f"Log file created at: {log_file}")

# Log Python paths
logger.info("Python Paths:")
for path in sys.path:
    logger.info(f"  - {path}")

def load_module_from_path(module_name, file_path):
    """
    Dynamically load a module from a given file path
    """
    try:
        logger.info(f"Attempting to load module {module_name} from {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Module file not found: {file_path}")
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Error loading module {module_name} from {file_path}:")
        logger.error(traceback.format_exc())
        raise

# Attempt to load the social_network module
try:
    # Try importing directly first
    from .social_network_impl.social_network import create_plugin
    logger.info("Successfully imported create_plugin directly")
except ImportError as direct_import_error:
    try:
        # If direct import fails, use the dynamic loading method
        impl_path = os.path.join(plugin_dir, 'social_network_impl', 'social_network.py')
        logger.info(f"Direct import failed. Attempting to load from: {impl_path}")
        
        social_network_module = load_module_from_path('social_network', impl_path)
        create_plugin = social_network_module.create_plugin
        logger.info("Successfully loaded create_plugin via dynamic loading")
    except Exception as dynamic_load_error:
        logger.error("Failed to import social_network module:")
        logger.error("Direct Import Error: %s", direct_import_error)
        logger.error("Dynamic Load Error: %s", dynamic_load_error)
        raise ImportError("Could not import social_network module") from dynamic_load_error

# Validate the create_plugin function
if not callable(create_plugin):
    raise ImportError("create_plugin is not a callable function")

# Optional: Log successful import
logger.info("Social Network Plugin loaded successfully")
logger.info(f"create_plugin function: {create_plugin}")

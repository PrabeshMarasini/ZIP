# Configuration constants for Zip File Explorer

class Config:
    """Application configuration constants"""
    
    # Application info
    APP_NAME = "CLI Zip File Explorer"
    APP_VERSION = "1.0.0"
    
    # Menu options
    MENU_OPTIONS = {
        '1': 'List Zip Contents',
        '2': 'Extract All Files',
        '3': 'Extract Selected Files',
        '4': 'Create Zip Archive',
        '5': 'Exit'
    }
    
    # File extensions
    ZIP_EXTENSIONS = ['.zip', '.ZIP']
    
    # Display settings
    MAX_FILENAME_DISPLAY = 50
    ITEMS_PER_PAGE = 20
    
    # Default directories
    DEFAULT_EXTRACT_DIR = "extracted_files"
    
    # Colors (for colorama)
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
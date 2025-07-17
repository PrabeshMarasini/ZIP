# Configuration constants for Modern ZIP Manager

class Config:
    """Application configuration constants"""
    
    # Application info
    APP_NAME = "Modern ZIP Manager"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "A modern, feature-rich ZIP archive manager"
    
    # File extensions
    ZIP_EXTENSIONS = ['.zip', '.ZIP']
    SUPPORTED_FORMATS = ['.zip', '.ZIP']
    
    # Display settings
    MAX_FILENAME_DISPLAY = 50
    ITEMS_PER_PAGE = 20
    
    # Default directories
    DEFAULT_EXTRACT_DIR = "extracted_files"
    
    # GUI Settings
    class GUI:
        # Window settings
        DEFAULT_WIDTH = 1000
        DEFAULT_HEIGHT = 700
        MIN_WIDTH = 800
        MIN_HEIGHT = 600
        
        # Colors and themes
        PRIMARY_COLOR = '#4a90e2'
        SUCCESS_COLOR = '#5cb85c'
        DANGER_COLOR = '#d9534f'
        WARNING_COLOR = '#f0ad4e'
        BACKGROUND_COLOR = '#f0f0f0'
        
        # Fonts
        DEFAULT_FONT = ('Segoe UI', 10)
        HEADER_FONT = ('Segoe UI', 12, 'bold')
        MONO_FONT = ('Consolas', 9)
        
        # Tree view settings
        ROW_HEIGHT = 28
        
    # File type mappings for icons and descriptions
    FILE_TYPES = {
        '.txt': {'type': 'Text', 'icon': '📄'},
        '.doc': {'type': 'Document', 'icon': '📄'},
        '.docx': {'type': 'Document', 'icon': '📄'},
        '.pdf': {'type': 'PDF', 'icon': '📄'},
        '.jpg': {'type': 'Image', 'icon': '🖼️'},
        '.jpeg': {'type': 'Image', 'icon': '🖼️'},
        '.png': {'type': 'Image', 'icon': '🖼️'},
        '.gif': {'type': 'Image', 'icon': '🖼️'},
        '.mp3': {'type': 'Audio', 'icon': '🎵'},
        '.wav': {'type': 'Audio', 'icon': '🎵'},
        '.mp4': {'type': 'Video', 'icon': '🎬'},
        '.avi': {'type': 'Video', 'icon': '🎬'},
        '.zip': {'type': 'Archive', 'icon': '📦'},
        '.rar': {'type': 'Archive', 'icon': '📦'},
        '.exe': {'type': 'Executable', 'icon': '⚙️'},
        '.py': {'type': 'Python', 'icon': '🐍'},
        '.js': {'type': 'JavaScript', 'icon': '📜'},
        '.html': {'type': 'Web', 'icon': '🌐'},
        '.css': {'type': 'Stylesheet', 'icon': '🎨'},
        '.xml': {'type': 'XML', 'icon': '📋'}
    }
    
    # Compression settings
    class Compression:
        DEFAULT_LEVEL = 6
        MIN_LEVEL = 0
        MAX_LEVEL = 9
        
        LEVEL_DESCRIPTIONS = {
            0: "No compression (fastest)",
            1: "Minimal compression",
            2: "Low compression",
            3: "Light compression", 
            4: "Medium-low compression",
            5: "Medium compression",
            6: "Standard compression (recommended)",
            7: "High compression",
            8: "Maximum compression",
            9: "Ultra compression (slowest)"
        }
# Modern ZIP Manager

A comprehensive, modern GUI-based ZIP archive manager built with Python and Tkinter.

## Features

### 🎨 Modern Interface
- Clean, intuitive graphical user interface
- WinRAR-inspired design with modern styling
- Drag & drop support for ZIP files
- Real-time search and filtering
- Responsive layout with resizable panels

### 📦 Archive Management
- **Open & Browse**: Load ZIP archives and browse contents with detailed information
- **Extract Files**: Extract all files or selected files with progress tracking
- **Create Archives**: Create new ZIP files from files/folders with compression options
- **Password Protection**: Full support for password-protected archives
- **Archive Testing**: Verify archive integrity

### 🔍 Advanced Features
- **File Search**: Real-time search within archive contents
- **File Details**: View comprehensive file information (size, compression ratio, dates)
- **Statistics**: Archive statistics and compression analysis
- **Multiple Selection**: Select and extract multiple files at once
- **Context Menus**: Right-click context menus for quick actions

### ⚙️ User Experience
- **Progress Tracking**: Real-time progress bars for long operations
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Preferences**: Customizable settings and options
- **Help System**: Built-in help and documentation
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd modern-zip-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pyminizip (for password-protected archives)

## Usage

### Opening Archives
- **File Menu**: Use File → Open ZIP or Ctrl+O
- **Drag & Drop**: Simply drag ZIP files into the application window
- **Recent Files**: Access recently opened archives (coming soon)

### Creating Archives
- **File Menu**: Use File → Create ZIP or Ctrl+N
- **Options**: Choose files/folders, set compression level, add password protection
- **Progress**: Monitor creation progress with real-time updates

### Extracting Files
- **Extract All**: Extract all files to a selected folder
- **Extract Selected**: Select specific files and extract them
- **Progress Tracking**: Monitor extraction progress with cancellation support

### Keyboard Shortcuts
- `Ctrl+O` - Open ZIP archive
- `Ctrl+N` - Create new ZIP archive
- `Ctrl+A` - Select all files
- `Ctrl+Q` - Exit application
- `F1` - Show help
- `Enter` - Extract selected files
- `Escape` - Deselect all

## Screenshots

*Screenshots coming soon...*

## Architecture

The application is built with a modular architecture:

- **main.py** - Application entry point and dependency checking
- **ui_main.py** - Modern GUI interface with all dialogs and windows
- **zip_manager.py** - Core ZIP operations and file handling
- **utils.py** - Utility functions for file operations and validation
- **config.py** - Configuration constants and settings

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Changelog

### Version 2.0.0
- Complete GUI redesign with modern interface
- Added drag & drop support
- Implemented real-time search and filtering
- Added progress tracking for all operations
- Enhanced file details and statistics
- Added keyboard shortcuts and context menus
- Improved error handling and user feedback
- Removed CLI interface in favor of full GUI experience

### Version 1.0.0
- Initial release with basic CLI interface
- Core ZIP operations (create, extract, list)
- Password protection support
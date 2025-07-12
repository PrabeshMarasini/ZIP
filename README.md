# CLI Zip File Explorer

A powerful command-line tool for managing ZIP archives with full password protection support and interactive menu system.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 🚀 Features

### Core Functionality
- **📋 List Archive Contents** - Browse zip files with detailed information
- **📦 Extract Files** - Extract all files or selected files by index
- **🗜️ Create Archives** - Compress files and folders into zip archives
- **🔒 Password Protection** - Full support for password-protected archives
- **📊 File Information** - View file sizes, compression ratios, and modification dates

### Advanced Features
- **🎯 Selective Extraction** - Extract specific files using index ranges (e.g., 1-5,8,10-12)
- **📈 Progress Tracking** - Real-time progress bars for operations
- **🔍 Smart Password Detection** - Automatically detects password-protected archives
- **⚙️ Compression Control** - Choose compression levels (0-9) when creating archives
- **🎨 Colorized Output** - Enhanced terminal experience with color coding
- **📁 Directory Integration** - Open extracted folders in file explorer

## 📋 Requirements

- Python 3.7 or higher
- Windows 10 (optimized), Linux, or macOS

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/prabeshmarasini/zip.git
   cd zip
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 📦 Dependencies

- `pyminizip` - For password-protected zip creation
- `colorama` - For cross-platform colored terminal output

## 🎮 Usage

### Quick Start
Simply run the application and follow the interactive menu:

```bash
python main.py
```

### Menu Options

1. **List Zip Contents** - Browse archive contents with detailed information
2. **Extract All Files** - Extract entire archive to a directory
3. **Extract Selected Files** - Extract specific files by index
4. **Create Zip Archive** - Create new zip archive from files/folders
5. **Exit** - Close the application

### Example Workflows

#### 📋 Listing Archive Contents
```
Select option: 1
Enter zip file path: example.zip
Enter password (if needed): ****
```

#### 📦 Extracting Files
```
Select option: 2
Enter zip file path: archive.zip
Enter extraction directory: ./extracted
Enter password (if needed): ****
```

#### 🗜️ Creating Archives
```
Select option: 4
Enter source path: ./my_folder
Enter output zip path: my_archive.zip
Create password-protected archive? (y/n): y
Enter password: ****
Enter compression level (0-9): 6
```

#### 🎯 Selective Extraction
```
Select option: 3
Enter zip file path: archive.zip
Enter file indices: 0,2,5-8,10
Enter extraction directory: ./selected_files
```

## 📁 Project Structure

```
cli-zip-explorer/
├── main.py              # Application entry point
├── menu_system.py       # Interactive menu system
├── zip_manager.py       # Core zip operations
├── utils.py             # Utility functions and validation
├── config.py            # Configuration constants
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## 🔧 Configuration

The application can be configured through `config.py`:

- **Display Settings**: Filename display length, items per page
- **Default Directories**: Default extraction directory
- **File Extensions**: Supported zip file extensions
- **Color Scheme**: Terminal color configuration

## 🎨 Features in Detail

### File Information Display
- File names with directory indicators
- Original and compressed file sizes
- Compression ratios
- Last modification dates
- Total archive statistics

### Index-Based File Selection
- Single indices: `0,2,5`
- Range selection: `1-5,8,10-15`
- Mixed selection: `0,3-7,12,15-20`

### Password Protection
- Automatic password detection
- Secure password input (hidden)
- Support for both extraction and creation
- Error handling for incorrect passwords

### Progress Tracking
- Real-time extraction progress
- File count and percentage completion
- Operation status indicators

## 🛡️ Error Handling

The application includes comprehensive error handling for:
- Invalid file paths
- Corrupted zip files
- Incorrect passwords
- Permission issues
- Network interruptions
- Insufficient disk space

## 🔒 Security Features

- **Secure Password Input** - Passwords are hidden during input
- **Memory Safety** - Passwords are not stored in memory longer than necessary
- **Path Validation** - Prevents directory traversal attacks
- **Safe Extraction** - Validates file paths before extraction

## 🚀 Performance

- **Efficient Memory Usage** - Streaming extraction for large files
- **Progress Feedback** - Real-time operation status
- **Optimized Compression** - Configurable compression levels
- **Batch Operations** - Handle multiple files efficiently

## 🐛 Troubleshooting

### Common Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**Permission denied:**
- Run with administrator privileges on Windows
- Use `sudo` on Linux/macOS if needed

**Password-protected archives not working:**
- Ensure `pyminizip` is properly installed
- Verify password is correct

**Colors not displaying:**
- Update terminal to support ANSI colors
- On Windows, use Windows Terminal or CMD with color support

## 📊 Supported Formats

- **ZIP** (`.zip`) - Full support
- **Password-protected ZIP** - Full support
- **Multi-volume archives** - Basic support
#!/usr/bin/env python3
"""
Modern ZIP Manager
A comprehensive GUI-based tool for managing zip archives

Features:
- Modern, intuitive graphical interface
- List zip file contents with detailed information
- Extract all files or selected files
- Create zip archives with optional password protection
- Drag & drop support
- Real-time progress tracking
- File preview capabilities
- Advanced compression settings

Author: Generated for zip file management
Version: 2.0.0
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import ui_main
    import tkinter as tk
    from tkinter import messagebox
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required files are in the same directory and dependencies are installed.")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['pyminizip', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", 
                f"Missing required packages: {', '.join(missing_packages)}\n\n"
                f"Please install them using:\n"
                f"pip install {' '.join(missing_packages)}")
            root.destroy()
        except:
            print(f"Missing required packages: {', '.join(missing_packages)}")
            print(f"Please install them using: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Main application entry point"""
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Launch the GUI application
        app = ui_main.ModernZipManagerUI()
        app.mainloop()

    except Exception as e:
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", f"Unexpected error: {e}")
            root.destroy()
        except:
            print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
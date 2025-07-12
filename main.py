#!/usr/bin/env python3
"""
CLI Zip File Explorer
A comprehensive command-line tool for managing zip archives

Features:
- List zip file contents with detailed information
- Extract all files or selected files by index
- Create zip archives with optional password protection
- Full support for password-protected archives
- Interactive menu system with input validation
- Cross-platform compatibility (Windows focus)

Author: Generated for zip file management
Version: 1.0.0
"""

import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from menu_system import MenuSystem
    from utils import ConsoleUtils
    from config import Config
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required files are in the same directory:")
    print("- main.py")
    print("- menu_system.py")
    print("- zip_manager.py")
    print("- utils.py")
    print("- config.py")
    print("- requirements.txt")
    sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = ['pyminizip', 'colorama']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Fore.RED}Missing required packages: {', '.join(missing_packages)}")
        print(f"{Fore.YELLOW}Please install them using:")
        print(f"{Fore.CYAN}pip install {' '.join(missing_packages)}")
        print(f"{Fore.YELLOW}Or use the requirements file:")
        print(f"{Fore.CYAN}pip install -r requirements.txt")
        return False
    
    return True

def display_welcome_message():
    """Display welcome message and basic information"""
    ConsoleUtils.print_header(f"Welcome to {Config.APP_NAME}")
    
    print(f"{Fore.CYAN}A powerful command-line tool for managing ZIP archives")
    print(f"{Fore.WHITE}")
    print(f"Features:")
    print(f"• List and browse zip file contents")
    print(f"• Extract all files or selected files by index")
    print(f"• Create new zip archives from files/folders")
    print(f"• Full password protection support")
    print(f"• Interactive menu system")
    print(f"• Cross-platform compatibility")
    print(f"")
    print(f"{Fore.GREEN}Version: {Config.APP_VERSION}")
    print(f"{Style.RESET_ALL}")

def main():
    """Main application entry point"""
    # Initialize colorama for Windows
    init(autoreset=True)
    
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Display welcome message
        display_welcome_message()
        
        # Pause before starting
        ConsoleUtils.pause()
        
        # Initialize and run menu system
        menu_system = MenuSystem()
        menu_system.run()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}")
        print(f"{Fore.YELLOW}Please report this issue if it persists.")
        sys.exit(1)
    finally:
        # Cleanup
        print(f"{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
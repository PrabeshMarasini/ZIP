import os
import sys
import getpass
from pathlib import Path
from typing import List, Optional, Union
from colorama import Fore, Style, init
from config import Config

# Initialize colorama for Windows
init(autoreset=True)

class InputValidator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Validate if file path exists and is a file"""
        path = Path(file_path)
        return path.exists() and path.is_file()
    
    @staticmethod
    def validate_zip_file(file_path: str) -> bool:
        """Validate if file is a zip file"""
        if not InputValidator.validate_file_path(file_path):
            return False
        
        path = Path(file_path)
        return path.suffix.lower() in [ext.lower() for ext in Config.ZIP_EXTENSIONS]
    
    @staticmethod
    def validate_directory(dir_path: str) -> bool:
        """Validate if directory path exists"""
        path = Path(dir_path)
        return path.exists() and path.is_dir()
    
    @staticmethod
    def validate_indices(indices_str: str, max_index: int) -> Optional[List[int]]:
        """Validate and parse comma-separated indices"""
        try:
            indices = []
            parts = indices_str.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range like "1-5"
                    start, end = map(int, part.split('-'))
                    if start <= end <= max_index and start >= 0:
                        indices.extend(range(start, end + 1))
                    else:
                        return None
                else:
                    # Single index
                    idx = int(part)
                    if 0 <= idx <= max_index:
                        indices.append(idx)
                    else:
                        return None
            
            return list(set(indices))  # Remove duplicates
        except ValueError:
            return None

class FileUtils:
    """File system utilities"""
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Get a safe filename for Windows"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def create_directory(dir_path: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error creating directory: {e}")
            return False
    
    @staticmethod
    def get_file_size_str(size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def truncate_filename(filename: str, max_length: int = Config.MAX_FILENAME_DISPLAY) -> str:
        """Truncate filename if too long"""
        if len(filename) <= max_length:
            return filename
        return filename[:max_length-3] + "..."

class ConsoleUtils:
    """Console output utilities"""
    
    @staticmethod
    def print_header(title: str):
        """Print formatted header"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}{title:^60}")
        print(f"{Fore.CYAN}{'='*60}")
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        print(f"{Fore.GREEN}✓ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        print(f"{Fore.RED}✗ {message}")
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message"""
        print(f"{Fore.YELLOW}⚠ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        print(f"{Fore.BLUE}ℹ {message}")
    
    @staticmethod
    def get_user_input(prompt: str, required: bool = True) -> str:
        """Get user input with validation"""
        while True:
            try:
                user_input = input(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}").strip()
                if required and not user_input:
                    ConsoleUtils.print_error("Input cannot be empty. Please try again.")
                    continue
                return user_input
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled by user.")
                return ""
            except EOFError:
                print(f"\n{Fore.RED}Unexpected end of input.")
                return ""
    
    @staticmethod
    def get_password(prompt: str = "Enter password") -> str:
        """Get password input (hidden)"""
        try:
            return getpass.getpass(f"{Fore.YELLOW}{prompt}: {Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.")
            return ""
    
    @staticmethod
    def confirm_action(prompt: str) -> bool:
        """Get yes/no confirmation from user"""
        while True:
            response = ConsoleUtils.get_user_input(f"{prompt} (y/n)", required=True).lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                ConsoleUtils.print_error("Please enter 'y' or 'n'.")
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def pause():
        """Pause and wait for user input"""
        input(f"\n{Fore.CYAN}Press Enter to continue...")

class PathUtils:
    """Path manipulation utilities"""
    
    @staticmethod
    def get_absolute_path(path: str) -> str:
        """Get absolute path from relative or absolute path"""
        return str(Path(path).resolve())
    
    @staticmethod
    def get_relative_path(path: str, base_path: str = None) -> str:
        """Get relative path from base path"""
        if base_path is None:
            base_path = os.getcwd()
        
        try:
            return str(Path(path).relative_to(Path(base_path)))
        except ValueError:
            return path
    
    @staticmethod
    def join_paths(*paths) -> str:
        """Join multiple paths safely"""
        return str(Path(*paths))
    
    @staticmethod
    def get_parent_directory(path: str) -> str:
        """Get parent directory of a path"""
        return str(Path(path).parent)
    
    @staticmethod
    def get_filename(path: str) -> str:
        """Get filename from path"""
        return Path(path).name
    
    @staticmethod
    def get_file_extension(path: str) -> str:
        """Get file extension"""
        return Path(path).suffix
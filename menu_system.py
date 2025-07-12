import os
import sys
import zipfile
from pathlib import Path
from colorama import Fore, Style
from utils import ConsoleUtils, InputValidator, FileUtils, PathUtils
from zip_manager import ZipManager
from config import Config

class MenuSystem:
    """Interactive menu system for the ZIP File Explorer"""
    
    def __init__(self):
        self.zip_manager = ZipManager()
        self.running = True
    
    def display_main_menu(self):
        """Display the main menu"""
        ConsoleUtils.print_header(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        
        print(f"{Fore.CYAN}Available Options:")
        for key, value in Config.MENU_OPTIONS.items():
            print(f"{Fore.YELLOW}{key}. {Fore.WHITE}{value}")
        
        print(f"\n{Fore.GREEN}Current Directory: {os.getcwd()}")
    
    def run(self):
        """Run the main menu loop"""
        ConsoleUtils.clear_screen()
        
        while self.running:
            try:
                self.display_main_menu()
                
                choice = ConsoleUtils.get_user_input("Select an option (1-5)")
                
                if choice == '1':
                    self.list_zip_contents_menu()
                elif choice == '2':
                    self.extract_all_files_menu()
                elif choice == '3':
                    self.extract_selected_files_menu()
                elif choice == '4':
                    self.create_zip_archive_menu()
                elif choice == '5':
                    self.exit_application()
                else:
                    ConsoleUtils.print_error("Invalid option. Please select 1-5.")
                    ConsoleUtils.pause()
                
                if self.running:
                    ConsoleUtils.clear_screen()
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Application interrupted by user.")
                self.exit_application()
            except Exception as e:
                ConsoleUtils.print_error(f"Unexpected error: {e}")
                ConsoleUtils.pause()
    
    def list_zip_contents_menu(self):
        """Menu for listing zip file contents"""
        ConsoleUtils.print_header("LIST ZIP CONTENTS")
        
        # Get zip file path
        zip_path = self.get_zip_file_path()
        if not zip_path:
            return
        
        # Check if password is needed
        password = None
        if self.check_password_needed(zip_path):
            password = ConsoleUtils.get_password("Enter zip password (or press Enter to skip)")
            if not password:
                password = None
        
        # List contents
        file_list = self.zip_manager.list_zip_contents(zip_path, password)
        
        if file_list is not None:
            self.zip_manager.display_zip_contents(file_list)
            
            # Show zip summary
            summary = self.zip_manager.get_zip_info_summary(zip_path)
            if summary:
                print(f"\n{Fore.CYAN}Archive Summary:")
                print(f"{Fore.WHITE}File: {summary['file_path']}")
                print(f"{Fore.WHITE}Archive size: {FileUtils.get_file_size_str(summary['file_size'])}")
        
        ConsoleUtils.pause()
    
    def extract_all_files_menu(self):
        """Menu for extracting all files from zip"""
        ConsoleUtils.print_header("EXTRACT ALL FILES")
        
        # Get zip file path
        zip_path = self.get_zip_file_path()
        if not zip_path:
            return
        
        # Get extraction directory
        extract_to = self.get_extraction_directory()
        if not extract_to:
            return
        
        # Check if password is needed
        password = None
        if self.check_password_needed(zip_path):
            password = ConsoleUtils.get_password("Enter zip password (or press Enter to skip)")
            if not password:
                password = None
        
        # Confirm extraction
        if not ConsoleUtils.confirm_action(f"Extract all files to '{extract_to}'?"):
            ConsoleUtils.print_info("Extraction cancelled.")
            ConsoleUtils.pause()
            return
        
        # Extract files
        success = self.zip_manager.extract_all_files(zip_path, extract_to, password)
        
        if success:
            ConsoleUtils.print_success("Extraction completed successfully!")
            if ConsoleUtils.confirm_action("Open extraction directory?"):
                self.open_directory(extract_to)
        else:
            ConsoleUtils.print_error("Extraction failed.")
        
        ConsoleUtils.pause()
    
    def extract_selected_files_menu(self):
        """Menu for extracting selected files from zip"""
        ConsoleUtils.print_header("EXTRACT SELECTED FILES")
        
        # Get zip file path
        zip_path = self.get_zip_file_path()
        if not zip_path:
            return
        
        # Check if password is needed
        password = None
        if self.check_password_needed(zip_path):
            password = ConsoleUtils.get_password("Enter zip password (or press Enter to skip)")
            if not password:
                password = None
        
        # List contents first
        file_list = self.zip_manager.list_zip_contents(zip_path, password)
        if file_list is None:
            return
        
        # Display contents with indices
        self.zip_manager.display_zip_contents(file_list)
        
        # Get file indices to extract
        indices = self.get_file_indices(len(file_list))
        if not indices:
            return
        
        # Get extraction directory
        extract_to = self.get_extraction_directory()
        if not extract_to:
            return
        
        # Show selected files
        print(f"\n{Fore.CYAN}Selected files to extract:")
        for i, idx in enumerate(indices):
            if 0 <= idx < len(file_list):
                file_info = file_list[idx]
                print(f"{Fore.WHITE}{i+1}. {file_info.filename}")
        
        # Confirm extraction
        if not ConsoleUtils.confirm_action(f"Extract {len(indices)} selected files to '{extract_to}'?"):
            ConsoleUtils.print_info("Extraction cancelled.")
            ConsoleUtils.pause()
            return
        
        # Extract selected files
        success = self.zip_manager.extract_selected_files(zip_path, extract_to, indices, password)
        
        if success:
            ConsoleUtils.print_success("Extraction completed successfully!")
            if ConsoleUtils.confirm_action("Open extraction directory?"):
                self.open_directory(extract_to)
        else:
            ConsoleUtils.print_error("Extraction failed.")
        
        ConsoleUtils.pause()
    
    def create_zip_archive_menu(self):
        """Menu for creating zip archives"""
        ConsoleUtils.print_header("CREATE ZIP ARCHIVE")
        
        # Get source path
        source_path = self.get_source_path()
        if not source_path:
            return
        
        # Get output zip path
        zip_path = self.get_output_zip_path()
        if not zip_path:
            return
        
        # Check if file exists
        if os.path.exists(zip_path):
            if not ConsoleUtils.confirm_action(f"File '{zip_path}' already exists. Overwrite?"):
                ConsoleUtils.print_info("Archive creation cancelled.")
                ConsoleUtils.pause()
                return
        
        # Ask for password protection
        password = None
        if ConsoleUtils.confirm_action("Create password-protected archive?"):
            password = ConsoleUtils.get_password("Enter password for archive")
            if not password:
                ConsoleUtils.print_warning("No password provided. Creating standard archive.")
                password = None
        
        # Get compression level
        compression_level = self.get_compression_level()
        
        # Show summary
        print(f"\n{Fore.CYAN}Archive Creation Summary:")
        print(f"{Fore.WHITE}Source: {source_path}")
        print(f"{Fore.WHITE}Archive: {zip_path}")
        print(f"{Fore.WHITE}Password protected: {'Yes' if password else 'No'}")
        print(f"{Fore.WHITE}Compression level: {compression_level}")
        
        # Confirm creation
        if not ConsoleUtils.confirm_action("Create archive?"):
            ConsoleUtils.print_info("Archive creation cancelled.")
            ConsoleUtils.pause()
            return
        
        # Create archive
        success = self.zip_manager.create_zip_archive(source_path, zip_path, password, compression_level)
        
        if success:
            ConsoleUtils.print_success("Archive created successfully!")
            
            # Show archive info
            if os.path.exists(zip_path):
                size = FileUtils.get_file_size_str(os.path.getsize(zip_path))
                print(f"{Fore.GREEN}Archive size: {size}")
            
            if ConsoleUtils.confirm_action("Open archive directory?"):
                self.open_directory(PathUtils.get_parent_directory(zip_path))
        else:
            ConsoleUtils.print_error("Archive creation failed.")
        
        ConsoleUtils.pause()
    
    def get_zip_file_path(self) -> str:
        """Get zip file path from user"""
        while True:
            zip_path = ConsoleUtils.get_user_input("Enter zip file path")
            if not zip_path:
                return ""
            
            # Expand path
            zip_path = PathUtils.get_absolute_path(zip_path)
            
            if not InputValidator.validate_file_path(zip_path):
                ConsoleUtils.print_error("File does not exist. Please try again.")
                continue
            
            if not InputValidator.validate_zip_file(zip_path):
                ConsoleUtils.print_error("File is not a valid zip file. Please try again.")
                continue
            
            return zip_path
    
    def get_extraction_directory(self) -> str:
        """Get extraction directory from user"""
        default_dir = Config.DEFAULT_EXTRACT_DIR
        
        extract_to = ConsoleUtils.get_user_input(f"Enter extraction directory (default: {default_dir})", required=False)
        
        if not extract_to:
            extract_to = default_dir
        
        extract_to = PathUtils.get_absolute_path(extract_to)
        
        # Create directory if it doesn't exist
        if not os.path.exists(extract_to):
            if ConsoleUtils.confirm_action(f"Directory '{extract_to}' does not exist. Create it?"):
                if not FileUtils.create_directory(extract_to):
                    ConsoleUtils.print_error("Failed to create directory.")
                    return ""
            else:
                return ""
        
        return extract_to
    
    def get_source_path(self) -> str:
        """Get source path for zip creation"""
        while True:
            source_path = ConsoleUtils.get_user_input("Enter path to file or directory to compress")
            if not source_path:
                return ""
            
            source_path = PathUtils.get_absolute_path(source_path)
            
            if not os.path.exists(source_path):
                ConsoleUtils.print_error("Path does not exist. Please try again.")
                continue
            
            return source_path
    
    def get_output_zip_path(self) -> str:
        """Get output zip file path"""
        while True:
            zip_path = ConsoleUtils.get_user_input("Enter output zip file path")
            if not zip_path:
                return ""
            
            zip_path = PathUtils.get_absolute_path(zip_path)
            
            # Add .zip extension if not present
            if not zip_path.lower().endswith('.zip'):
                zip_path += '.zip'
            
            # Check if parent directory exists
            parent_dir = PathUtils.get_parent_directory(zip_path)
            if not os.path.exists(parent_dir):
                ConsoleUtils.print_error(f"Parent directory does not exist: {parent_dir}")
                continue
            
            return zip_path
    
    def get_file_indices(self, max_index: int) -> list:
        """Get file indices from user"""
        while True:
            indices_str = ConsoleUtils.get_user_input(
                f"Enter file indices to extract (0-{max_index-1}, comma-separated, ranges like 1-5 allowed)"
            )
            
            if not indices_str:
                return []
            
            indices = InputValidator.validate_indices(indices_str, max_index - 1)
            
            if indices is None:
                ConsoleUtils.print_error("Invalid indices format. Please try again.")
                ConsoleUtils.print_info("Examples: '0,2,5' or '1-3,7,9-11'")
                continue
            
            if not indices:
                ConsoleUtils.print_error("No valid indices provided.")
                continue
            
            return indices
    
    def get_compression_level(self) -> int:
        """Get compression level from user"""
        while True:
            level_str = ConsoleUtils.get_user_input("Enter compression level (0-9, default: 6)", required=False)
            
            if not level_str:
                return 6
            
            try:
                level = int(level_str)
                if 0 <= level <= 9:
                    return level
                else:
                    ConsoleUtils.print_error("Compression level must be between 0-9.")
            except ValueError:
                ConsoleUtils.print_error("Invalid compression level. Please enter a number 0-9.")
    
    def check_password_needed(self, zip_path: str) -> bool:
        """Check if zip file might need a password"""
        try:
            # Try to open without password first
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Try to read the first file
                file_list = zip_file.infolist()
                if file_list:
                    first_file = next((f for f in file_list if not f.is_dir()), None)
                    if first_file:
                        try:
                            zip_file.read(first_file.filename, pwd=None)
                            return False  # No password needed
                        except RuntimeError:
                            return True  # Might need password
            return False
        except Exception:
            return True  # Assume password might be needed
    
    def open_directory(self, directory_path: str):
        """Open directory in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(directory_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{directory_path}"' if sys.platform == 'darwin' else f'xdg-open "{directory_path}"')
        except Exception as e:
            ConsoleUtils.print_error(f"Could not open directory: {e}")
    
    def exit_application(self):
        """Exit the application"""
        ConsoleUtils.print_info("Thank you for using CLI Zip File Explorer!")
        self.running = False
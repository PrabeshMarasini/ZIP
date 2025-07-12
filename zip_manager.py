import os
import zipfile
import pyminizip
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from colorama import Fore, Style
from utils import FileUtils, ConsoleUtils, PathUtils
from config import Config

class ZipInfo:
    """Information about a file in a zip archive"""
    
    def __init__(self, zip_info: zipfile.ZipInfo):
        self.filename = zip_info.filename
        self.file_size = zip_info.file_size
        self.compress_size = zip_info.compress_size
        self.date_time = zip_info.date_time
        self.is_dir = zip_info.is_dir()
        self.crc = zip_info.CRC
        
    def get_formatted_date(self) -> str:
        """Get formatted date string"""
        try:
            dt = datetime(*self.date_time)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return "Unknown"
    
    def get_compression_ratio(self) -> float:
        """Calculate compression ratio"""
        if self.file_size == 0:
            return 0.0
        return (1 - (self.compress_size / self.file_size)) * 100

class ZipManager:
    """Main class for managing zip file operations"""
    
    def __init__(self):
        self.current_zip_path = None
        self.current_zip_info = None
        self.password = None
    
    def list_zip_contents(self, zip_path: str, password: Optional[str] = None) -> Optional[List[ZipInfo]]:
        """List contents of a zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Try to access the zip file with password if provided
                if password:
                    zip_file.setpassword(password.encode())
                
                # Get file list
                file_list = []
                for info in zip_file.infolist():
                    try:
                        # Test if we can access the file (for password-protected archives)
                        if password and not info.is_dir():
                            zip_file.read(info.filename, pwd=password.encode())
                        file_list.append(ZipInfo(info))
                    except (RuntimeError, zipfile.BadZipFile):
                        # Skip files we can't access
                        continue
                
                self.current_zip_path = zip_path
                self.current_zip_info = file_list
                self.password = password
                return file_list
                
        except FileNotFoundError:
            ConsoleUtils.print_error(f"Zip file not found: {zip_path}")
        except zipfile.BadZipFile:
            ConsoleUtils.print_error(f"Invalid zip file: {zip_path}")
        except RuntimeError as e:
            if "Bad password" in str(e):
                ConsoleUtils.print_error("Incorrect password for zip file")
            else:
                ConsoleUtils.print_error(f"Error reading zip file: {e}")
        except Exception as e:
            ConsoleUtils.print_error(f"Unexpected error: {e}")
        
        return None
    
    def display_zip_contents(self, file_list: List[ZipInfo]):
        """Display zip contents in a formatted table"""
        if not file_list:
            ConsoleUtils.print_warning("No files found in the archive")
            return
        
        ConsoleUtils.print_header("ZIP FILE CONTENTS")
        
        # Header
        header = f"{'Index':<6} {'Name':<40} {'Size':<12} {'Compressed':<12} {'Ratio':<8} {'Date':<20}"
        print(f"{Fore.CYAN}{header}")
        print(f"{Fore.CYAN}{'-' * len(header)}")
        
        # File entries
        for i, file_info in enumerate(file_list):
            name = FileUtils.truncate_filename(file_info.filename, 38)
            size_str = FileUtils.get_file_size_str(file_info.file_size)
            comp_size_str = FileUtils.get_file_size_str(file_info.compress_size)
            ratio = f"{file_info.get_compression_ratio():.1f}%"
            date_str = file_info.get_formatted_date()
            
            # Color coding
            if file_info.is_dir:
                color = Fore.BLUE
                name = f"{name}/"
            else:
                color = Fore.WHITE
            
            print(f"{color}{i:<6} {name:<40} {size_str:<12} {comp_size_str:<12} {ratio:<8} {date_str:<20}")
        
        print(f"\n{Fore.GREEN}Total files: {len([f for f in file_list if not f.is_dir])}")
        print(f"{Fore.GREEN}Total directories: {len([f for f in file_list if f.is_dir])}")
        
        # Calculate totals
        total_size = sum(f.file_size for f in file_list if not f.is_dir)
        total_compressed = sum(f.compress_size for f in file_list if not f.is_dir)
        
        if total_size > 0:
            overall_ratio = (1 - (total_compressed / total_size)) * 100
            print(f"{Fore.GREEN}Total size: {FileUtils.get_file_size_str(total_size)}")
            print(f"{Fore.GREEN}Compressed size: {FileUtils.get_file_size_str(total_compressed)}")
            print(f"{Fore.GREEN}Overall compression: {overall_ratio:.1f}%")
    
    def extract_all_files(self, zip_path: str, extract_to: str, password: Optional[str] = None) -> bool:
        """Extract all files from zip archive"""
        try:
            # Create extraction directory
            if not FileUtils.create_directory(extract_to):
                return False
            
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Set password if provided
                if password:
                    zip_file.setpassword(password.encode())
                
                # Get total number of files to extract
                files_to_extract = [f for f in zip_file.infolist() if not f.is_dir()]
                total_files = len(files_to_extract)
                
                if total_files == 0:
                    ConsoleUtils.print_warning("No files to extract")
                    return True
                
                ConsoleUtils.print_info(f"Extracting {total_files} files to: {extract_to}")
                
                # Extract files with progress
                extracted_count = 0
                for file_info in files_to_extract:
                    try:
                        # Extract file
                        zip_file.extract(file_info, extract_to, pwd=password.encode() if password else None)
                        extracted_count += 1
                        
                        # Show progress
                        progress = (extracted_count / total_files) * 100
                        print(f"\r{Fore.CYAN}Progress: {progress:.1f}% ({extracted_count}/{total_files})", end='', flush=True)
                        
                    except Exception as e:
                        ConsoleUtils.print_error(f"\nFailed to extract {file_info.filename}: {e}")
                
                print()  # New line after progress
                ConsoleUtils.print_success(f"Successfully extracted {extracted_count}/{total_files} files")
                return extracted_count > 0
                
        except FileNotFoundError:
            ConsoleUtils.print_error(f"Zip file not found: {zip_path}")
        except zipfile.BadZipFile:
            ConsoleUtils.print_error(f"Invalid zip file: {zip_path}")
        except RuntimeError as e:
            if "Bad password" in str(e):
                ConsoleUtils.print_error("Incorrect password for zip file")
            else:
                ConsoleUtils.print_error(f"Error extracting files: {e}")
        except Exception as e:
            ConsoleUtils.print_error(f"Unexpected error during extraction: {e}")
        
        return False
    
    def extract_selected_files(self, zip_path: str, extract_to: str, indices: List[int], password: Optional[str] = None) -> bool:
        """Extract selected files by indices"""
        try:
            # Create extraction directory
            if not FileUtils.create_directory(extract_to):
                return False
            
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Set password if provided
                if password:
                    zip_file.setpassword(password.encode())
                
                file_list = zip_file.infolist()
                
                # Validate indices
                max_index = len(file_list) - 1
                valid_indices = [i for i in indices if 0 <= i <= max_index]
                
                if not valid_indices:
                    ConsoleUtils.print_error("No valid file indices provided")
                    return False
                
                ConsoleUtils.print_info(f"Extracting {len(valid_indices)} selected files to: {extract_to}")
                
                # Extract selected files
                extracted_count = 0
                for i, index in enumerate(valid_indices):
                    file_info = file_list[index]
                    
                    if file_info.is_dir():
                        ConsoleUtils.print_warning(f"Skipping directory: {file_info.filename}")
                        continue
                    
                    try:
                        # Extract file
                        zip_file.extract(file_info, extract_to, pwd=password.encode() if password else None)
                        extracted_count += 1
                        
                        # Show progress
                        progress = ((i + 1) / len(valid_indices)) * 100
                        print(f"\r{Fore.CYAN}Progress: {progress:.1f}% ({i + 1}/{len(valid_indices)})", end='', flush=True)
                        
                    except Exception as e:
                        ConsoleUtils.print_error(f"\nFailed to extract {file_info.filename}: {e}")
                
                print()  # New line after progress
                ConsoleUtils.print_success(f"Successfully extracted {extracted_count} files")
                return extracted_count > 0
                
        except FileNotFoundError:
            ConsoleUtils.print_error(f"Zip file not found: {zip_path}")
        except zipfile.BadZipFile:
            ConsoleUtils.print_error(f"Invalid zip file: {zip_path}")
        except RuntimeError as e:
            if "Bad password" in str(e):
                ConsoleUtils.print_error("Incorrect password for zip file")
            else:
                ConsoleUtils.print_error(f"Error extracting files: {e}")
        except Exception as e:
            ConsoleUtils.print_error(f"Unexpected error during extraction: {e}")
        
        return False
    
    def create_zip_archive(self, source_path: str, zip_path: str, password: Optional[str] = None, compression_level: int = 6) -> bool:
        """Create a zip archive from a directory or file"""
        try:
            source_path = Path(source_path)
            
            if not source_path.exists():
                ConsoleUtils.print_error(f"Source path does not exist: {source_path}")
                return False
            
            # Collect files to compress
            files_to_compress = []
            
            if source_path.is_file():
                files_to_compress.append((source_path, source_path.name))
            elif source_path.is_dir():
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(source_path)
                        files_to_compress.append((file_path, str(arc_name)))
            
            if not files_to_compress:
                ConsoleUtils.print_error("No files found to compress")
                return False
            
            ConsoleUtils.print_info(f"Creating zip archive: {zip_path}")
            ConsoleUtils.print_info(f"Files to compress: {len(files_to_compress)}")
            
            # Create zip archive
            if password:
                # Use pyminizip for password-protected archives
                return self._create_password_protected_zip(files_to_compress, zip_path, password, compression_level)
            else:
                # Use standard zipfile for non-protected archives
                return self._create_standard_zip(files_to_compress, zip_path, compression_level)
                
        except Exception as e:
            ConsoleUtils.print_error(f"Unexpected error during archive creation: {e}")
            return False
    
    def _create_standard_zip(self, files_to_compress: List[Tuple[Path, str]], zip_path: str, compression_level: int) -> bool:
        """Create standard zip archive without password"""
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zip_file:
                for i, (file_path, arc_name) in enumerate(files_to_compress):
                    try:
                        zip_file.write(file_path, arc_name)
                        
                        # Show progress
                        progress = ((i + 1) / len(files_to_compress)) * 100
                        print(f"\r{Fore.CYAN}Progress: {progress:.1f}% ({i + 1}/{len(files_to_compress)})", end='', flush=True)
                        
                    except Exception as e:
                        ConsoleUtils.print_error(f"\nFailed to compress {file_path}: {e}")
            
            print()  # New line after progress
            ConsoleUtils.print_success(f"Successfully created zip archive: {zip_path}")
            return True
            
        except Exception as e:
            ConsoleUtils.print_error(f"Error creating zip archive: {e}")
            return False
    
    def _create_password_protected_zip(self, files_to_compress: List[Tuple[Path, str]], zip_path: str, password: str, compression_level: int) -> bool:
        """Create password-protected zip archive using pyminizip"""
        try:
            # pyminizip requires file paths as strings
            file_paths = [str(file_path) for file_path, _ in files_to_compress]
            arc_names = [arc_name for _, arc_name in files_to_compress]
            
            ConsoleUtils.print_info("Creating password-protected archive...")
            
            # Create password-protected zip
            pyminizip.compress_multiple(
                file_paths,
                arc_names,
                zip_path,
                password,
                compression_level
            )
            
            ConsoleUtils.print_success(f"Successfully created password-protected zip archive: {zip_path}")
            return True
            
        except Exception as e:
            ConsoleUtils.print_error(f"Error creating password-protected zip archive: {e}")
            return False
    
    def get_zip_info_summary(self, zip_path: str) -> Optional[Dict[str, Any]]:
        """Get summary information about a zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                file_list = zip_file.infolist()
                
                total_files = len([f for f in file_list if not f.is_dir()])
                total_dirs = len([f for f in file_list if f.is_dir()])
                total_size = sum(f.file_size for f in file_list if not f.is_dir())
                total_compressed = sum(f.compress_size for f in file_list if not f.is_dir())
                
                return {
                    'total_files': total_files,
                    'total_directories': total_dirs,
                    'total_size': total_size,
                    'total_compressed': total_compressed,
                    'compression_ratio': (1 - (total_compressed / total_size)) * 100 if total_size > 0 else 0,
                    'file_path': zip_path,
                    'file_size': os.path.getsize(zip_path)
                }
                
        except Exception as e:
            ConsoleUtils.print_error(f"Error getting zip info: {e}")
            return None
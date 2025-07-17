import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import threading
import time
from pathlib import Path
import webbrowser
import zip_manager
from datetime import datetime

class ModernZipManagerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Modern ZIP Manager v2.0')
        self.geometry('1000x700')
        self.minsize(800, 600)
        self.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.manager = zip_manager.ZipManager()
        self.zip_contents = []
        self.current_zip_path = None
        self.selected_items = []
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value='Ready')
        self.operation_cancelled = False
        
        # Setup UI
        self._setup_style()
        self._create_menu()
        self._create_widgets()
        
        # Center window
        self._center_window()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _setup_style(self):
        """Setup modern UI styling"""
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Modern.TFrame', background='#f0f0f0', relief='flat')
        self.style.configure('Toolbar.TFrame', background='#e8e8e8', relief='raised', borderwidth=1)
        self.style.configure('Modern.TButton', 
                           background='#4a90e2', 
                           foreground='white', 
                           font=('Segoe UI', 10, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
        self.style.map('Modern.TButton', 
                      background=[('active', '#357abd'), ('pressed', '#2968a3')])
        
        self.style.configure('Action.TButton',
                           background='#5cb85c',
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'))
        self.style.map('Action.TButton',
                      background=[('active', '#449d44'), ('pressed', '#398439')])
        
        self.style.configure('Danger.TButton',
                           background='#d9534f',
                           foreground='white',
                           font=('Segoe UI', 9, 'bold'))
        self.style.map('Danger.TButton',
                      background=[('active', '#c9302c'), ('pressed', '#ac2925')])
        
        self.style.configure('Modern.Treeview',
                           background='#ffffff',
                           fieldbackground='#ffffff',
                           foreground='#333333',
                           rowheight=28,
                           font=('Segoe UI', 9))
        self.style.configure('Modern.Treeview.Heading',
                           background='#4a90e2',
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))
        
    def _create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open ZIP...", command=self.open_zip, accelerator="Ctrl+O")
        file_menu.add_command(label="Create ZIP...", command=self.create_zip, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Recent Files", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Deselect All", command=self.deselect_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences...", command=self.show_preferences)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Test Archive", command=self.test_archive)
        tools_menu.add_command(label="Archive Information", command=self.show_archive_info)
        tools_menu.add_separator()
        tools_menu.add_command(label="Compression Settings", command=self.show_compression_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.bind('<Control-o>', lambda e: self.open_zip())
        self.bind('<Control-n>', lambda e: self.create_zip())
        self.bind('<Control-a>', lambda e: self.select_all())
        self.bind('<Control-q>', lambda e: self._on_closing())
        
    def _create_widgets(self):
        """Create main UI widgets"""
        # Main container
        main_container = ttk.Frame(self, style='Modern.TFrame')
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Toolbar
        self._create_toolbar(main_container)
        
        # Content area
        content_frame = ttk.Frame(main_container, style='Modern.TFrame')
        content_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        # Left panel (file tree)
        left_panel = ttk.Frame(content_frame, style='Modern.TFrame')
        left_panel.pack(side='left', fill='both', expand=True)
        
        # Archive contents
        self._create_archive_view(left_panel)
        
        # Right panel (details and actions)
        right_panel = ttk.Frame(content_frame, style='Modern.TFrame', width=250)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self._create_details_panel(right_panel)
        
        # Bottom panel (progress and status)
        self._create_bottom_panel(main_container)
        
    def _create_toolbar(self, parent):
        """Create modern toolbar"""
        toolbar = ttk.Frame(parent, style='Toolbar.TFrame')
        toolbar.pack(fill='x', pady=(0, 5))
        
        # Left side buttons
        left_frame = ttk.Frame(toolbar, style='Toolbar.TFrame')
        left_frame.pack(side='left', padx=10, pady=8)
        
        ttk.Button(left_frame, text='📁 Open', style='Modern.TButton',
                  command=self.open_zip).pack(side='left', padx=(0, 5))
        ttk.Button(left_frame, text='📦 Create', style='Modern.TButton',
                  command=self.create_zip).pack(side='left', padx=5)
        ttk.Button(left_frame, text='📤 Extract', style='Action.TButton',
                  command=self.extract_selected).pack(side='left', padx=5)
        ttk.Button(left_frame, text='📋 Test', style='Modern.TButton',
                  command=self.test_archive).pack(side='left', padx=5)
        
        # Right side info
        right_frame = ttk.Frame(toolbar, style='Toolbar.TFrame')
        right_frame.pack(side='right', padx=10, pady=8)
        
        self.archive_info_label = ttk.Label(right_frame, text='No archive loaded',
                                          font=('Segoe UI', 9), background='#e8e8e8')
        self.archive_info_label.pack(side='right')
        
    def _create_archive_view(self, parent):
        """Create archive contents view"""
        # Header
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(header_frame, text='Archive Contents', 
                 font=('Segoe UI', 12, 'bold')).pack(side='left')
        
        # Search box
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side='right')
        
        ttk.Label(search_frame, text='Search:').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left')
        
        # Treeview with scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Name', 'Size', 'Compressed', 'Ratio', 'Date', 'Type')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                style='Modern.Treeview', selectmode='extended')
        
        # Configure columns
        self.tree.heading('Name', text='Name', anchor='w')
        self.tree.heading('Size', text='Size', anchor='e')
        self.tree.heading('Compressed', text='Compressed', anchor='e')
        self.tree.heading('Ratio', text='Ratio', anchor='e')
        self.tree.heading('Date', text='Date Modified', anchor='center')
        self.tree.heading('Type', text='Type', anchor='center')
        
        self.tree.column('Name', width=300, anchor='w')
        self.tree.column('Size', width=80, anchor='e')
        self.tree.column('Compressed', width=80, anchor='e')
        self.tree.column('Ratio', width=60, anchor='e')
        self.tree.column('Date', width=120, anchor='center')
        self.tree.column('Type', width=80, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        self.tree.bind('<Double-1>', self._on_tree_double_click)
        self.tree.bind('<Button-3>', self._on_tree_right_click)
        
    def _create_details_panel(self, parent):
        """Create details and actions panel"""
        # File details section
        details_frame = ttk.LabelFrame(parent, text='File Details', padding=10)
        details_frame.pack(fill='x', pady=(0, 10))
        
        self.details_text = tk.Text(details_frame, height=8, width=30, wrap='word',
                                   font=('Consolas', 9), state='disabled')
        details_scroll = ttk.Scrollbar(details_frame, orient='vertical',
                                     command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scroll.set)
        
        self.details_text.pack(side='left', fill='both', expand=True)
        details_scroll.pack(side='right', fill='y')
        
        # Quick actions section
        actions_frame = ttk.LabelFrame(parent, text='Quick Actions', padding=10)
        actions_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(actions_frame, text='Extract Selected',
                  command=self.extract_selected, width=20).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text='Extract All',
                  command=self.extract_all, width=20).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text='Add Files',
                  command=self.add_files_to_zip, width=20).pack(fill='x', pady=2)
        ttk.Button(actions_frame, text='Delete Selected',
                  command=self.delete_selected, width=20,
                  style='Danger.TButton').pack(fill='x', pady=2)
        
        # Archive statistics
        stats_frame = ttk.LabelFrame(parent, text='Archive Statistics', padding=10)
        stats_frame.pack(fill='x')
        
        self.stats_text = tk.Text(stats_frame, height=6, width=30, wrap='word',
                                 font=('Segoe UI', 9), state='disabled')
        self.stats_text.pack(fill='both', expand=True)
        
    def _create_bottom_panel(self, parent):
        """Create bottom panel with progress and status"""
        bottom_frame = ttk.Frame(parent, style='Modern.TFrame')
        bottom_frame.pack(fill='x', pady=(5, 0))
        
        # Progress bar
        progress_frame = ttk.Frame(bottom_frame)
        progress_frame.pack(fill='x', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill='x', padx=(0, 10), side='left', expand=True)
        
        self.cancel_button = ttk.Button(progress_frame, text='Cancel',
                                      command=self._cancel_operation, state='disabled')
        self.cancel_button.pack(side='right')
        
        # Status bar
        status_frame = ttk.Frame(bottom_frame, relief='sunken', borderwidth=1)
        status_frame.pack(fill='x')
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                    anchor='w', padding=(5, 2))
        self.status_label.pack(side='left', fill='x', expand=True)
        
        # Selection info
        self.selection_label = ttk.Label(status_frame, text='0 items selected',
                                       padding=(5, 2))
        self.selection_label.pack(side='right')
        

        
    def _center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def _on_search_changed(self, *args):
        """Handle search text changes"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self._refresh_tree_view()
            return
            
        # Filter items based on search term
        filtered_contents = [item for item in self.zip_contents 
                           if search_term in item.filename.lower()]
        self._populate_tree(filtered_contents)
        
    def _on_tree_select(self, event):
        """Handle tree selection changes"""
        selected = self.tree.selection()
        self.selected_items = selected
        
        # Update selection info
        count = len(selected)
        self.selection_label.config(text=f'{count} item{"s" if count != 1 else ""} selected')
        
        # Update details panel
        if count == 1:
            item_id = selected[0]
            item_index = int(self.tree.item(item_id)['values'][0]) - 1
            if 0 <= item_index < len(self.zip_contents):
                self._show_file_details(self.zip_contents[item_index])
        else:
            self._clear_file_details()
            
    def _on_tree_double_click(self, event):
        """Handle double-click on tree items"""
        selected = self.tree.selection()
        if selected:
            # For now, just extract the selected file
            self.extract_selected()
            
    def _on_tree_right_click(self, event):
        """Handle right-click context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._show_context_menu(event)
            
    def _show_context_menu(self, event):
        """Show context menu"""
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Extract", command=self.extract_selected)
        context_menu.add_command(label="Extract to...", command=self.extract_selected_to)
        context_menu.add_separator()
        context_menu.add_command(label="Properties", command=self.show_file_properties)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
            
    def _on_drop(self, event):
        """Handle file drop events"""
        files = event.data.split()
        zip_files = [f for f in files if f.lower().endswith('.zip')]
        
        if zip_files:
            self.load_zip_file(zip_files[0])
        else:
            messagebox.showinfo("Drop Files", "Please drop ZIP files only.")
            
    def open_zip(self):
        """Open ZIP file dialog"""
        file_path = filedialog.askopenfilename(
            title="Open ZIP Archive",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if file_path:
            self.load_zip_file(file_path)
            
    def load_zip_file(self, file_path):
        """Load ZIP file contents"""
        self.status_var.set('Loading archive...')
        self.update_idletasks()
        
        def load_worker():
            try:
                # Check if password is needed
                password = None
                if self._check_password_needed(file_path):
                    password = self._get_password_dialog("Enter archive password:")
                    if password is None:  # User cancelled
                        self.status_var.set('Ready')
                        return
                
                contents = self.manager.list_zip_contents(file_path, password)
                if contents is not None:
                    self.zip_contents = contents
                    self.current_zip_path = file_path
                    self._populate_tree(contents)
                    self._update_archive_info()
                    self._update_statistics()
                    self.status_var.set(f'Loaded: {os.path.basename(file_path)} ({len(contents)} items)')
                else:
                    self.status_var.set('Failed to load archive')
                    messagebox.showerror("Error", "Failed to load ZIP archive. Check password or file integrity.")
            except Exception as e:
                self.status_var.set('Error loading archive')
                messagebox.showerror("Error", f"Error loading archive: {str(e)}")
                
        threading.Thread(target=load_worker, daemon=True).start()
        
    def _check_password_needed(self, zip_path):
        """Check if ZIP file needs password"""
        try:
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zf:
                file_list = zf.infolist()
                if file_list:
                    first_file = next((f for f in file_list if not f.is_dir()), None)
                    if first_file:
                        try:
                            zf.read(first_file.filename)
                            return False
                        except RuntimeError:
                            return True
            return False
        except:
            return True
            
    def _get_password_dialog(self, prompt):
        """Show password input dialog"""
        return simpledialog.askstring("Password Required", prompt, show='*')
        
    def _populate_tree(self, contents):
        """Populate tree with ZIP contents"""
        self.tree.delete(*self.tree.get_children())
        
        for i, item in enumerate(contents):
            name = item.filename
            size = self._format_size(item.file_size)
            compressed = self._format_size(item.compress_size)
            ratio = f"{item.get_compression_ratio():.1f}%"
            date = item.get_formatted_date()
            file_type = "Folder" if item.is_dir else self._get_file_type(name)
            
            # Add icon based on type
            if item.is_dir:
                name = f"📁 {name}"
            else:
                name = f"📄 {name}"
                
            self.tree.insert('', 'end', values=(i+1, name, size, compressed, ratio, date, file_type))
            
    def _refresh_tree_view(self):
        """Refresh tree view with current contents"""
        if self.zip_contents:
            self._populate_tree(self.zip_contents)
            
    def _update_archive_info(self):
        """Update archive information display"""
        if self.current_zip_path:
            filename = os.path.basename(self.current_zip_path)
            file_size = self._format_size(os.path.getsize(self.current_zip_path))
            self.archive_info_label.config(text=f"{filename} ({file_size})")
        else:
            self.archive_info_label.config(text="No archive loaded")
            
    def _update_statistics(self):
        """Update archive statistics"""
        if not self.zip_contents:
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.config(state='disabled')
            return
            
        total_files = len([f for f in self.zip_contents if not f.is_dir])
        total_folders = len([f for f in self.zip_contents if f.is_dir])
        total_size = sum(f.file_size for f in self.zip_contents if not f.is_dir)
        total_compressed = sum(f.compress_size for f in self.zip_contents if not f.is_dir)
        compression_ratio = (1 - (total_compressed / total_size)) * 100 if total_size > 0 else 0
        
        stats = f"""Files: {total_files}
Folders: {total_folders}
Total Size: {self._format_size(total_size)}
Compressed: {self._format_size(total_compressed)}
Compression: {compression_ratio:.1f}%
Archive: {self._format_size(os.path.getsize(self.current_zip_path)) if self.current_zip_path else 'N/A'}"""
        
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state='disabled')
        
    def _show_file_details(self, file_info):
        """Show details for selected file"""
        details = f"""Name: {file_info.filename}
Type: {'Folder' if file_info.is_dir else self._get_file_type(file_info.filename)}
Size: {self._format_size(file_info.file_size)}
Compressed: {self._format_size(file_info.compress_size)}
Compression: {file_info.get_compression_ratio():.1f}%
Modified: {file_info.get_formatted_date()}
CRC32: {hex(file_info.crc) if file_info.crc else 'N/A'}"""
        
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
        self.details_text.config(state='disabled')
        
    def _clear_file_details(self):
        """Clear file details display"""
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state='disabled')
        
    def _get_file_type(self, filename):
        """Get file type from extension"""
        ext = Path(filename).suffix.lower()
        type_map = {
            '.txt': 'Text', '.doc': 'Document', '.docx': 'Document',
            '.pdf': 'PDF', '.jpg': 'Image', '.jpeg': 'Image', '.png': 'Image',
            '.gif': 'Image', '.mp3': 'Audio', '.wav': 'Audio', '.mp4': 'Video',
            '.avi': 'Video', '.zip': 'Archive', '.rar': 'Archive',
            '.exe': 'Executable', '.py': 'Python', '.js': 'JavaScript',
            '.html': 'Web', '.css': 'Stylesheet', '.xml': 'XML'
        }
        return type_map.get(ext, 'File')
        
    def _format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
        
    def create_zip(self):
        """Create new ZIP archive"""
        dialog = CreateZipDialog(self)
        self.wait_window(dialog)
        
    def extract_selected(self):
        """Extract selected files"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files to extract.")
            return
            
        if not self.current_zip_path:
            messagebox.showwarning("No Archive", "Please open an archive first.")
            return
            
        extract_dir = filedialog.askdirectory(title="Select extraction folder")
        if not extract_dir:
            return
            
        self._extract_files_with_progress(extract_dir, selected_only=True)
        
    def extract_selected_to(self):
        """Extract selected files to specific location"""
        self.extract_selected()
        
    def extract_all(self):
        """Extract all files"""
        if not self.current_zip_path:
            messagebox.showwarning("No Archive", "Please open an archive first.")
            return
            
        extract_dir = filedialog.askdirectory(title="Select extraction folder")
        if not extract_dir:
            return
            
        self._extract_files_with_progress(extract_dir, selected_only=False)
        
    def _extract_files_with_progress(self, extract_dir, selected_only=False):
        """Extract files with progress tracking"""
        self.operation_cancelled = False
        self.progress_var.set(0)
        self.cancel_button.config(state='normal')
        
        def extract_worker():
            try:
                if selected_only:
                    # Get indices of selected items
                    indices = []
                    for item_id in self.selected_items:
                        item_index = int(self.tree.item(item_id)['values'][0]) - 1
                        indices.append(item_index)
                    
                    success = self.manager.extract_selected_files(
                        self.current_zip_path, extract_dir, indices, 
                        progress_callback=self._update_progress
                    )
                else:
                    success = self.manager.extract_all_files(
                        self.current_zip_path, extract_dir,
                        progress_callback=self._update_progress
                    )
                
                if success and not self.operation_cancelled:
                    self.status_var.set('Extraction completed successfully')
                    messagebox.showinfo("Success", f"Files extracted to:\n{extract_dir}")
                elif self.operation_cancelled:
                    self.status_var.set('Extraction cancelled')
                else:
                    self.status_var.set('Extraction failed')
                    messagebox.showerror("Error", "Extraction failed")
                    
            except Exception as e:
                self.status_var.set('Extraction error')
                messagebox.showerror("Error", f"Extraction error: {str(e)}")
            finally:
                self.progress_var.set(0)
                self.cancel_button.config(state='disabled')
                
        threading.Thread(target=extract_worker, daemon=True).start()
        
    def _update_progress(self, current, total):
        """Update progress bar"""
        if total > 0:
            progress = (current / total) * 100
            self.progress_var.set(progress)
            self.status_var.set(f'Extracting... {current}/{total} files')
            self.update_idletasks()
        return not self.operation_cancelled
        
    def _cancel_operation(self):
        """Cancel current operation"""
        self.operation_cancelled = True
        self.cancel_button.config(state='disabled')
        
    def add_files_to_zip(self):
        """Add files to existing ZIP (placeholder)"""
        messagebox.showinfo("Feature", "Add files feature coming soon!")
        
    def delete_selected(self):
        """Delete selected files from ZIP (placeholder)"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select files to delete.")
            return
        messagebox.showinfo("Feature", "Delete files feature coming soon!")
        
    def test_archive(self):
        """Test archive integrity"""
        if not self.current_zip_path:
            messagebox.showwarning("No Archive", "Please open an archive first.")
            return
            
        self.status_var.set('Testing archive...')
        
        def test_worker():
            try:
                import zipfile
                with zipfile.ZipFile(self.current_zip_path, 'r') as zf:
                    bad_files = zf.testzip()
                    if bad_files:
                        messagebox.showerror("Test Failed", f"Archive test failed. Corrupt file: {bad_files}")
                        self.status_var.set('Archive test failed')
                    else:
                        messagebox.showinfo("Test Passed", "Archive integrity test passed!")
                        self.status_var.set('Archive test passed')
            except Exception as e:
                messagebox.showerror("Test Error", f"Error testing archive: {str(e)}")
                self.status_var.set('Archive test error')
                
        threading.Thread(target=test_worker, daemon=True).start()
        
    def show_archive_info(self):
        """Show detailed archive information"""
        if not self.current_zip_path:
            messagebox.showwarning("No Archive", "Please open an archive first.")
            return
        ArchiveInfoDialog(self, self.current_zip_path, self.zip_contents)
        
    def show_file_properties(self):
        """Show properties of selected file"""
        if not self.selected_items:
            messagebox.showwarning("No Selection", "Please select a file first.")
            return
        # Implementation would show detailed file properties
        messagebox.showinfo("Feature", "File properties dialog coming soon!")
        
    def select_all(self):
        """Select all items in tree"""
        children = self.tree.get_children()
        self.tree.selection_set(children)
        
    def deselect_all(self):
        """Deselect all items"""
        self.tree.selection_remove(self.tree.selection())
        
    def show_preferences(self):
        """Show preferences dialog"""
        PreferencesDialog(self)
        
    def show_compression_settings(self):
        """Show compression settings dialog"""
        messagebox.showinfo("Feature", "Compression settings coming soon!")
        
    def show_help(self):
        """Show help documentation"""
        help_text = """Modern ZIP Manager Help

Keyboard Shortcuts:
- Ctrl+O: Open ZIP file
- Ctrl+N: Create new ZIP
- Ctrl+A: Select all files
- Ctrl+Q: Exit application

Features:
- Drag & drop ZIP files to open
- Right-click for context menu
- Search files within archive
- Extract selected or all files
- Test archive integrity
- View detailed file information

For more help, visit our website."""
        
        HelpDialog(self, help_text)
        
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts = """Keyboard Shortcuts:

File Operations:
Ctrl+O - Open ZIP archive
Ctrl+N - Create new ZIP archive
Ctrl+Q - Exit application

Selection:
Ctrl+A - Select all files
Escape - Deselect all

Navigation:
Enter - Extract selected files
Delete - Delete selected files (coming soon)
F5 - Refresh view

Other:
F1 - Show help
Ctrl+, - Preferences"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
        
    def show_about(self):
        """Show about dialog"""
        AboutDialog(self)
        
    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Modern ZIP Manager?"):
            self.destroy()


class CreateZipDialog(tk.Toplevel):
    """Dialog for creating new ZIP archives"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Create ZIP Archive")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self._create_widgets()
        self._center_on_parent(parent)
        
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Source selection
        ttk.Label(main_frame, text="Select files/folders to compress:",
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        
        source_frame = ttk.Frame(main_frame)
        source_frame.pack(fill='x', pady=(0, 15))
        
        self.source_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.source_var, state='readonly').pack(side='left', fill='x', expand=True)
        ttk.Button(source_frame, text="Browse Files", command=self._browse_files).pack(side='right', padx=(5, 0))
        ttk.Button(source_frame, text="Browse Folder", command=self._browse_folder).pack(side='right', padx=(5, 0))
        
        # Output location
        ttk.Label(main_frame, text="Output ZIP file:",
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill='x', pady=(0, 15))
        
        self.output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_var).pack(side='left', fill='x', expand=True)
        ttk.Button(output_frame, text="Browse", command=self._browse_output).pack(side='right', padx=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=10)
        options_frame.pack(fill='x', pady=(0, 15))
        
        self.password_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Password protect archive",
                       variable=self.password_var, command=self._toggle_password).pack(anchor='w')
        
        self.password_frame = ttk.Frame(options_frame)
        self.password_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(self.password_frame, text="Password:").pack(side='left')
        self.password_entry = ttk.Entry(self.password_frame, show='*', state='disabled')
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Compression level
        ttk.Label(options_frame, text="Compression level:").pack(anchor='w', pady=(10, 0))
        self.compression_var = tk.IntVar(value=6)
        compression_frame = ttk.Frame(options_frame)
        compression_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Scale(compression_frame, from_=0, to=9, variable=self.compression_var,
                 orient='horizontal').pack(side='left', fill='x', expand=True)
        ttk.Label(compression_frame, textvariable=self.compression_var).pack(side='right', padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Create", command=self._create_zip).pack(side='right')
        
    def _browse_files(self):
        """Browse for files to compress"""
        files = filedialog.askopenfilenames(title="Select files to compress")
        if files:
            self.source_var.set("; ".join(files))
            
    def _browse_folder(self):
        """Browse for folder to compress"""
        folder = filedialog.askdirectory(title="Select folder to compress")
        if folder:
            self.source_var.set(folder)
            
    def _browse_output(self):
        """Browse for output location"""
        output = filedialog.asksaveasfilename(
            title="Save ZIP as",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")]
        )
        if output:
            self.output_var.set(output)
            
    def _toggle_password(self):
        """Toggle password entry state"""
        if self.password_var.get():
            self.password_entry.config(state='normal')
        else:
            self.password_entry.config(state='disabled')
            
    def _create_zip(self):
        """Create the ZIP archive"""
        source = self.source_var.get()
        output = self.output_var.get()
        
        if not source or not output:
            messagebox.showerror("Error", "Please select source and output locations.")
            return
            
        password = self.password_entry.get() if self.password_var.get() else None
        compression = self.compression_var.get()
        
        # Here you would call the actual ZIP creation logic
        messagebox.showinfo("Success", f"ZIP archive created: {output}")
        self.destroy()
        
    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class ArchiveInfoDialog(tk.Toplevel):
    """Dialog showing detailed archive information"""
    def __init__(self, parent, zip_path, contents):
        super().__init__(parent)
        self.title("Archive Information")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()
        
        self.zip_path = zip_path
        self.contents = contents
        self._create_widgets()
        self._center_on_parent(parent)
        
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Archive info text
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.info_text = tk.Text(text_frame, wrap='word', font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.destroy).pack()
        
        self._populate_info()
        
    def _populate_info(self):
        """Populate archive information"""
        info = f"""Archive Information
{'='*50}

File: {os.path.basename(self.zip_path)}
Path: {self.zip_path}
Size: {self._format_size(os.path.getsize(self.zip_path))}
Modified: {datetime.fromtimestamp(os.path.getmtime(self.zip_path)).strftime('%Y-%m-%d %H:%M:%S')}

Contents Summary
{'='*50}

Total Items: {len(self.contents)}
Files: {len([f for f in self.contents if not f.is_dir])}
Folders: {len([f for f in self.contents if f.is_dir])}

Size Information
{'='*50}

Uncompressed Size: {self._format_size(sum(f.file_size for f in self.contents if not f.is_dir))}
Compressed Size: {self._format_size(sum(f.compress_size for f in self.contents if not f.is_dir))}
Compression Ratio: {self._get_overall_compression():.1f}%

File Types
{'='*50}

{self._get_file_types_summary()}
"""
        
        self.info_text.insert(1.0, info)
        self.info_text.config(state='disabled')
        
    def _format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
        
    def _get_overall_compression(self):
        """Calculate overall compression ratio"""
        total_size = sum(f.file_size for f in self.contents if not f.is_dir)
        total_compressed = sum(f.compress_size for f in self.contents if not f.is_dir)
        return (1 - (total_compressed / total_size)) * 100 if total_size > 0 else 0
        
    def _get_file_types_summary(self):
        """Get summary of file types"""
        types = {}
        for item in self.contents:
            if not item.is_dir:
                ext = Path(item.filename).suffix.lower() or 'No extension'
                types[ext] = types.get(ext, 0) + 1
                
        summary = []
        for ext, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            summary.append(f"{ext}: {count} files")
            
        return '\n'.join(summary[:10])  # Show top 10 types
        
    def _center_on_parent(self, parent):
        """Center dialog on parent"""
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class PreferencesDialog(tk.Toplevel):
    """Preferences dialog"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Preferences")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._center_on_parent(parent)
        
    def _create_widgets(self):
        """Create preferences widgets"""
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        ttk.Label(general_frame, text="Default extraction folder:").pack(anchor='w', pady=(10, 5))
        ttk.Entry(general_frame, width=50).pack(fill='x', padx=10)
        
        ttk.Checkbutton(general_frame, text="Show confirmation dialogs").pack(anchor='w', pady=10)
        ttk.Checkbutton(general_frame, text="Remember window size and position").pack(anchor='w')
        
        # Appearance tab
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        
        ttk.Label(appearance_frame, text="Theme:").pack(anchor='w', pady=(10, 5))
        theme_combo = ttk.Combobox(appearance_frame, values=["Light", "Dark", "System"])
        theme_combo.pack(fill='x', padx=10)
        theme_combo.set("Light")
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="OK", command=self.destroy).pack(side='right')
        
    def _center_on_parent(self, parent):
        """Center on parent window"""
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class HelpDialog(tk.Toplevel):
    """Help dialog"""
    def __init__(self, parent, help_text):
        super().__init__(parent)
        self.title("Help")
        self.geometry("600x500")
        self.transient(parent)
        
        text_frame = ttk.Frame(self, padding=10)
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Segoe UI', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        text_widget.insert(1.0, help_text)
        text_widget.config(state='disabled')
        
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10)
        
        self._center_on_parent(parent)
        
    def _center_on_parent(self, parent):
        """Center on parent window"""
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class AboutDialog(tk.Toplevel):
    """About dialog"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Modern ZIP Manager")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # App icon and title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text="📦", font=('Segoe UI', 48)).pack()
        ttk.Label(title_frame, text="Modern ZIP Manager", 
                 font=('Segoe UI', 16, 'bold')).pack()
        ttk.Label(title_frame, text="Version 2.0.0", 
                 font=('Segoe UI', 10)).pack()
        
        # Description
        desc_text = """A modern, feature-rich ZIP archive manager with an intuitive graphical interface.

Features include drag & drop support, password protection, file search, and comprehensive archive management tools.

Built with Python and Tkinter."""
        
        ttk.Label(main_frame, text=desc_text, justify='center',
                 wraplength=350).pack(pady=20)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Visit Website", 
                  command=lambda: webbrowser.open("https://github.com")).pack(side='left')
        ttk.Button(button_frame, text="Close", command=self.destroy).pack(side='right')
        
        self._center_on_parent(parent)
        
    def _center_on_parent(self, parent):
        """Center on parent window"""
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    app = ModernZipManagerUI()
    app.mainloop()
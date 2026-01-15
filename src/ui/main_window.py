"""
Main window layout and structure for Nuitka GUI.
"""
import tkinter as tk
from tkinter import ttk

from ..utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from .tab_basic import TabBasic
from .tab_modules import TabModules
from .tab_data import TabData
from .tab_platform import TabPlatform
from .tab_advanced import TabAdvanced
from .tab_output import TabOutput


class MainWindow:
    """Main window containing tabs and output panel."""

    def __init__(self, parent, config, app):
        """
        Initialize main window.

        Args:
            parent: Parent widget (root window)
            config: ConfigManager instance
            app: Main application instance
        """
        self.parent = parent
        self.config = config
        self.app = app

        # Set window size
        self.parent.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.parent.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Create main container
        self.main_container = ttk.Frame(parent)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook (tabs)
        self.create_notebook()

        # Create bottom panel (output + buttons)
        self.create_bottom_panel()

        # Create status bar
        self.create_status_bar()

        # Load initial values from config
        self.load_from_config()

    def create_notebook(self):
        """Create tabbed interface."""
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create tabs
        self.tab_basic = TabBasic(self.notebook, self.config)
        self.tab_modules = TabModules(self.notebook, self.config)
        self.tab_data = TabData(self.notebook, self.config)
        self.tab_platform = TabPlatform(self.notebook, self.config)
        self.tab_advanced = TabAdvanced(self.notebook, self.config)
        self.tab_output = TabOutput(self.notebook, self.config)

        # Add tabs to notebook
        self.notebook.add(self.tab_basic, text="Basic Settings")
        self.notebook.add(self.tab_modules, text="Modules & Packages")
        self.notebook.add(self.tab_data, text="Data & Resources")
        self.notebook.add(self.tab_platform, text="Platform Specific")
        self.notebook.add(self.tab_advanced, text="Advanced Options")
        self.notebook.add(self.tab_output, text="Output & Plugins")

    def create_bottom_panel(self):
        """Create bottom panel with output and buttons."""
        bottom_frame = ttk.Frame(self.main_container)
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Output label
        ttk.Label(bottom_frame, text="Compilation Output:").pack(anchor=tk.W)

        # Output text with scrollbar
        output_frame = ttk.Frame(bottom_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scrollbar = ttk.Scrollbar(output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(
            output_frame,
            height=10,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Button frame
        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        self.compile_btn = ttk.Button(
            btn_frame,
            text="Compile",
            command=self.app.on_compile,
            style='Accent.TButton'
        )
        self.compile_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.app.on_cancel_compile,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="Clear Output",
            command=self.clear_output
        ).pack(side=tk.LEFT)

        ttk.Button(
            btn_frame,
            text="Show Command",
            command=self.app.on_show_command
        ).pack(side=tk.RIGHT)

    def create_status_bar(self):
        """Create status bar at bottom."""
        self.status_bar = ttk.Label(
            self.parent,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_compiling(self, is_compiling):
        """
        Update UI for compilation state.

        Args:
            is_compiling: True if compilation is running
        """
        if is_compiling:
            self.compile_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.NORMAL)
        else:
            self.compile_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)

    def append_output(self, text):
        """
        Append text to output panel.

        Args:
            text: Text to append
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_output(self):
        """Clear output panel."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state=tk.DISABLED)

    def update_status(self, message):
        """
        Update status bar message.

        Args:
            message: Status message
        """
        self.status_bar.config(text=message)

    def load_from_config(self):
        """Load values from config into UI."""
        self.tab_basic.load_from_config()
        self.tab_modules.load_from_config()
        self.tab_data.load_from_config()
        self.tab_platform.load_from_config()
        self.tab_advanced.load_from_config()
        self.tab_output.load_from_config()

    def save_to_config(self):
        """Save values from UI into config."""
        self.tab_basic.save_to_config()
        self.tab_modules.save_to_config()
        self.tab_data.save_to_config()
        self.tab_platform.save_to_config()
        self.tab_advanced.save_to_config()
        self.tab_output.save_to_config()

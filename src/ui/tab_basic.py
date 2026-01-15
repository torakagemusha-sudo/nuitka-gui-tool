"""
Basic settings tab for Nuitka GUI.
"""
import tkinter as tk
from tkinter import ttk
from ..utils.constants import MODES, COMPILERS, PYTHON_FLAGS
from .widgets import FileSelectFrame, add_tooltip


class TabBasic(ttk.Frame):
    """Tab for basic compilation settings."""

    def __init__(self, parent, config):
        """
        Initialize basic settings tab.

        Args:
            parent: Parent widget
            config: ConfigManager instance
        """
        super().__init__(parent)
        self.config = config
        self.widgets = {}

        # Create scrollable frame
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_widgets()

    def create_widgets(self):
        """Create widgets for basic tab."""
        # Input file section
        input_frame = ttk.LabelFrame(self.scrollable_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.widgets['input_file'] = FileSelectFrame(
            input_frame,
            "Python Script:",
            mode='file',
            file_types=[('Python files', '*.py'), ('All files', '*.*')]
        )
        self.widgets['input_file'].pack(fill=tk.X)
        add_tooltip(self.widgets['input_file'], "Main Python script to compile")

        # Compilation mode section
        mode_frame = ttk.LabelFrame(self.scrollable_frame, text="Compilation Mode", padding=10)
        mode_frame.pack(fill=tk.X, padx=5, pady=5)

        self.widgets['mode'] = tk.StringVar(value='standalone')
        for i, (label, value) in enumerate(MODES):
            rb = ttk.Radiobutton(
                mode_frame,
                text=label,
                variable=self.widgets['mode'],
                value=value
            )
            rb.grid(row=i, column=0, sticky=tk.W, pady=2)

            # Add tooltips
            if value == 'standalone':
                add_tooltip(rb, "Creates a standalone executable with all dependencies")
            elif value == 'onefile':
                add_tooltip(rb, "Packages everything into a single executable file")
            elif value == 'accelerated':
                add_tooltip(rb, "Compiles to an extension module (faster to build)")

        # Output section
        output_frame = ttk.LabelFrame(self.scrollable_frame, text="Output Settings", padding=10)
        output_frame.pack(fill=tk.X, padx=5, pady=5)

        self.widgets['output_dir'] = FileSelectFrame(
            output_frame,
            "Output Directory:",
            mode='directory'
        )
        self.widgets['output_dir'].pack(fill=tk.X, pady=(0, 5))
        add_tooltip(self.widgets['output_dir'], "Where to place the compiled output (leave empty for default)")

        output_file_frame = ttk.Frame(output_frame)
        output_file_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(output_file_frame, text="Output Filename:").pack(side=tk.LEFT, padx=(0, 5))
        self.widgets['output_filename'] = ttk.Entry(output_file_frame, width=40)
        self.widgets['output_filename'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        add_tooltip(self.widgets['output_filename'], "Custom output filename (leave empty for automatic)")

        self.widgets['remove_output'] = tk.BooleanVar(value=True)
        cb = ttk.Checkbutton(
            output_frame,
            text="Remove build directory after compilation",
            variable=self.widgets['remove_output']
        )
        cb.pack(anchor=tk.W)
        add_tooltip(cb, "Clean up temporary build files after successful compilation")

        # Compiler selection section
        compiler_frame = ttk.LabelFrame(self.scrollable_frame, text="Compiler Selection", padding=10)
        compiler_frame.pack(fill=tk.X, padx=5, pady=5)

        self.widgets['compiler'] = tk.StringVar(value='auto')
        for i, (label, value) in enumerate(COMPILERS):
            rb = ttk.Radiobutton(
                compiler_frame,
                text=label,
                variable=self.widgets['compiler'],
                value=value
            )
            rb.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=10, pady=2)

        # MSVC version (only shown if MSVC selected)
        msvc_frame = ttk.Frame(compiler_frame)
        msvc_frame.grid(row=len(COMPILERS) // 2 + 1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        ttk.Label(msvc_frame, text="MSVC Version:").pack(side=tk.LEFT, padx=(0, 5))
        self.widgets['msvc_version'] = ttk.Combobox(
            msvc_frame,
            values=['latest', '2022', '2019', '2017'],
            width=15,
            state='readonly'
        )
        self.widgets['msvc_version'].set('latest')
        self.widgets['msvc_version'].pack(side=tk.LEFT)

        # Python flags section
        flags_frame = ttk.LabelFrame(self.scrollable_frame, text="Python Behavior Flags", padding=10)
        flags_frame.pack(fill=tk.X, padx=5, pady=5)

        self.widgets['python_flags'] = {}
        for i, (flag_name, description) in enumerate(PYTHON_FLAGS):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                flags_frame,
                text=f"{flag_name}",
                variable=var
            )
            cb.grid(row=i, column=0, sticky=tk.W, pady=2)
            add_tooltip(cb, description)
            self.widgets['python_flags'][flag_name] = var

    def load_from_config(self):
        """Load values from config."""
        # Input file
        input_file = self.config.get('basic.input_file', '')
        self.widgets['input_file'].set_path(input_file)

        # Mode
        mode = self.config.get('basic.mode', 'standalone')
        self.widgets['mode'].set(mode)

        # Output
        output_dir = self.config.get('basic.output_dir', '')
        self.widgets['output_dir'].set_path(output_dir)

        output_filename = self.config.get('basic.output_filename', '')
        self.widgets['output_filename'].delete(0, tk.END)
        if output_filename:
            self.widgets['output_filename'].insert(0, output_filename)

        remove_output = self.config.get('basic.remove_output', True)
        self.widgets['remove_output'].set(remove_output)

        # Compiler
        compiler = self.config.get('basic.compiler', 'auto')
        self.widgets['compiler'].set(compiler)

        msvc_version = self.config.get('basic.msvc_version', 'latest')
        self.widgets['msvc_version'].set(msvc_version)

        # Python flags
        python_flags = self.config.get('basic.python_flags', [])
        for flag_name, var in self.widgets['python_flags'].items():
            var.set(flag_name in python_flags)

    def save_to_config(self):
        """Save values to config."""
        # Input file
        self.config.set('basic.input_file', self.widgets['input_file'].get_path())

        # Mode
        self.config.set('basic.mode', self.widgets['mode'].get())

        # Output
        self.config.set('basic.output_dir', self.widgets['output_dir'].get_path())
        self.config.set('basic.output_filename', self.widgets['output_filename'].get())
        self.config.set('basic.remove_output', self.widgets['remove_output'].get())

        # Compiler
        self.config.set('basic.compiler', self.widgets['compiler'].get())
        self.config.set('basic.msvc_version', self.widgets['msvc_version'].get())

        # Python flags
        selected_flags = [
            flag_name
            for flag_name, var in self.widgets['python_flags'].items()
            if var.get()
        ]
        self.config.set('basic.python_flags', selected_flags)

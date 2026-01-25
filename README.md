# Nuitka GUI

A graphical user interface for the Nuitka Python Compiler. This tool provides an easy-to-use interface for all Nuitka command-line options, eliminating the need to memorize complex flags and parameters.

## Features

- **Complete Coverage**: Supports all Nuitka command-line options through an intuitive tabbed interface
- **Platform-Aware**: Automatically detects your operating system and shows relevant options (Windows, macOS, Linux)
- **Smart Defaults**: Intelligent default values and tooltips to guide you
- **Configuration Management**: Save and load compilation configurations as JSON files
- **Real-Time Output**: View compilation progress and output in real-time
- **Command Preview**: See the exact Nuitka command that will be executed
- **Modern UI**: Built with PySide6 (Qt for Python) featuring a clean, professional interface
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux

## Requirements

- Python 3.8 or higher
- PySide6 (`pip install PySide6`)
- Nuitka (`pip install nuitka`)

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/nuitka-gui-tool.git
   cd nuitka-gui-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Nuitka:
   ```bash
   pip install nuitka
   ```

## Usage

Run the GUI:
```bash
python main.py
```

Or on Windows, you can double-click `main.py`

### Basic Workflow

1. **Select Input File**: Choose your main Python script
2. **Configure Options**: Use the tabs to configure:
   - **Basic Settings**: Compilation mode, output settings, compiler selection
   - **Modules & Packages**: Control which modules to include/exclude
   - **Data & Resources**: Include data files, resources, and assets
   - **Platform Specific**: Windows icons, macOS bundles, version information
   - **Advanced Options**: Optimization, debugging, compatibility settings
   - **Output & Plugins**: Enable plugins, control output verbosity

3. **Save Configuration** (optional): Save your settings for reuse
4. **Compile**: Click the "Compile" button
5. **Monitor Progress**: Watch the real-time compilation output

## Tab Overview

### Basic Settings
- Input Python script selection
- Compilation modes (Standalone, One-File, App Bundle, Accelerated)
- Output directory and filename
- Compiler selection (MSVC, MinGW64, Clang, Zig)
- Python behavior flags

### Modules & Packages
- Control import following
- Force include specific packages/modules
- Exclude modules from compilation

### Data & Resources
- Include package data
- Add data files and directories
- Exclude patterns
- DLL handling

### Platform Specific
**Windows**:
- Application icons
- Console mode control
- UAC settings
- Version information (product name, version, copyright, etc.)

**macOS**:
- App bundle creation
- Bundle identifier
- App icons and resources

**Linux**:
- Application icons

### Advanced Options
- Link-time optimization (LTO)
- Parallel compilation jobs
- Debug mode
- Compatibility options
- Cache control

### Output & Plugins
- Output verbosity control
- Progress bar styles
- Nuitka plugins (PySide6, numpy, matplotlib, PyQt, etc.)
- Warning configuration

## Configuration Files

Save your compilation settings as JSON files for reuse:

```json
{
  "basic": {
    "input_file": "main.py",
    "mode": "onefile",
    "compiler": "msvc"
  },
  "modules": {
    "follow_imports": true,
    "include_packages": ["numpy", "pandas"]
  },
  "platform": {
    "windows": {
      "icon": "app.ico",
      "product_name": "My Application",
      "file_version": "1.0.0.0"
    }
  }
}
```

Example configurations are available in the `configs/examples/` directory.

## Keyboard Shortcuts

- **Ctrl+N**: New configuration
- **Ctrl+O**: Open configuration
- **Ctrl+S**: Save configuration
- **Ctrl+Q**: Quit

## Compiling the GUI Itself

Since this is a PySide6 application, you can compile it with Nuitka:

```bash
python -m nuitka --standalone --enable-plugin=pyside6 main.py
```

For a single-file executable:

```bash
python -m nuitka --onefile --enable-plugin=pyside6 main.py
```

Or use the GUI itself to compile itself!

## Project Structure

```
nuitka-gui-tool/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── configs/            # Configuration file examples
├── assets/             # Application resources
└── src/
    ├── app.py          # Main application class
    ├── core/           # Core functionality
    │   ├── command_builder.py    # Nuitka command generation
    │   ├── config.py            # Configuration management
    │   ├── executor.py          # Compilation execution
    │   ├── platform_detector.py # OS detection
    │   ├── setting_definitions.py # Settings schema
    │   └── validator.py         # Input validation
    ├── ui/             # User interface components
    │   ├── main_window.py       # Main window
    │   ├── styles.py            # UI styling
    │   ├── tab_*.py             # Tab implementations
    │   └── widgets.py           # Custom widgets
    └── utils/          # Utility functions
        └── constants.py         # Application constants
```

## Tips

- **Standalone Mode**: Recommended for distributing applications - includes all dependencies
- **One-File Mode**: Creates a single executable (larger file, slightly slower startup)
- **Plugins**: Enable the appropriate plugin for frameworks you use (pyside6, numpy, pyqt5, etc.)
- **Follow Imports**: Usually should be enabled for standalone/onefile modes
- **Icons**: Windows accepts .ico or .png files, macOS accepts .icns or .png files

## Troubleshooting

**"Nuitka Not Found"**: Install Nuitka with `pip install nuitka`

**Compilation Errors**: Check the output panel for detailed error messages. Common issues:
- Missing C compiler (Windows: install Visual Studio or MinGW)
- Missing modules (use --include-package flag)
- Data files not included (use Data & Resources tab)

**Large Executables**: One-file mode creates larger files. Consider:
- Using standalone mode instead
- Enabling LTO (link-time optimization)
- Excluding unnecessary packages

## Platform Notes

### Windows
- MSVC (Visual Studio) compiler is recommended
- MinGW64 is automatically downloaded if needed
- UAC elevation can be configured for admin requirements

### macOS
- Clang compiler (Xcode Command Line Tools) required
- Can create .app bundles
- Code signing supported

### Linux
- GCC or Clang compiler required
- System-dependent binary output

## Learn More

- [Nuitka Official Documentation](https://nuitka.net/user-documentation/user-manual.html)
- [Nuitka GitHub Repository](https://github.com/Nuitka/Nuitka)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)

## Known Issues

Some bugs and improvements are being tracked and will be addressed in future releases:

- Error handling improvements needed for file operations
- Better user feedback for configuration errors
- Enhanced validation for compilation settings
- Platform-specific feature testing

See the [Issues](../../issues) page for detailed bug reports and planned improvements.

## Development Status

This project is somewhat maintained. As a solo developer overseeing approximately 50 ongoing projects, engagement, response times, and enthusiasm may vary significantly.

## License

This GUI tool is provided as-is for use with Nuitka. Nuitka itself is licensed under the Apache License 2.0.

## Contributing

Suggestions and improvements are welcome, though please note that due to the maintainer's workload across multiple projects, responses and merges may take time. This tool aims to make Nuitka more accessible to everyone.
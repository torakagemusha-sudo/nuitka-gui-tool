# Nuitka GUI

[![CodeQL](https://github.com/torakagemusha-sudo/nuitka-gui-tool/actions/workflows/codeql.yml/badge.svg)](https://github.com/torakagemusha-sudo/nuitka-gui-tool/actions/workflows/codeql.yml)

## Screenshot

![Nuitka GUI Interface](docs/screenshot.png)

## About

A PySide6 GUI for Nuitka — compile Python to executable without memorising CLI flags.

## Quick Start

```bash
pip install PySide6 nuitka
pip install -r requirements.txt
python main.py
```

## Features

This GUI exposes all major Nuitka command-line flags through an intuitive interface:

- **Standalone Mode** – Create self-contained executables without Python installation
- **One-File Packaging** – Bundle everything into a single `.exe` or binary
- **Custom Icon** – Set application icons easily
- **Plugin Management** – Enable/disable Nuitka plugins for optimization
- **Output Directory** – Specify custom build output paths
- **Compilation Options** – Control optimization levels, module inclusion, and more
- **Dark/Light Theme** – Fluent Design stylesheet with theme toggle
- **Configuration Persistence** – Save and load compilation profiles as JSON
- **Real-time Build Output** – Monitor compilation progress in the integrated console
- **Command Preview** – View the generated Nuitka command before execution
- **Cross-platform UI** – Responsive design adapts to your screen

## Platform Support

- **Windows x64** – Fully tested and supported
- **Linux** – Status unknown; contributions welcome
- **macOS** – Status unknown; contributions welcome

## Requirements

- **Python 3.10+**
- **Nuitka** – Must be installed separately: `pip install nuitka`
- **PySide6** – See `requirements.txt`

## Installation & Usage

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install PySide6 nuitka
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Development

To run tests and development tools:

```bash
pip install -r requirements-dev.txt
pytest
```

## License

See LICENSE file for details.
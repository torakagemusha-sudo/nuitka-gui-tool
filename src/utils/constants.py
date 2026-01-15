"""
Constants for the Nuitka GUI application.
"""

APP_NAME = "Nuitka GUI"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Nuitka GUI Tool"

# Compilation modes
MODES = [
    ("Accelerated (Module)", "accelerated"),
    ("Standalone", "standalone"),
    ("One-File", "onefile"),
    ("App Bundle (macOS)", "app"),
]

# Compiler options
COMPILERS = [
    ("Auto-detect", "auto"),
    ("MSVC (Windows)", "msvc"),
    ("MinGW64", "mingw64"),
    ("Clang", "clang"),
    ("Zig", "zig"),
]

# Python flags with descriptions
PYTHON_FLAGS = [
    ("isolated", "Ignore PYTHONPATH and user site-packages (-I)"),
    ("no_site", "Don't import site module (-S)"),
    ("no_asserts", "Disable assert statements (-O)"),
    ("no_docstrings", "Remove docstrings"),
    ("no_warnings", "Suppress warnings"),
    ("safe_path", "Prevent current directory lookup (-P)"),
    ("static_hashes", "Disable hash randomization"),
    ("unbuffered", "Force unbuffered stdout/stderr (-u)"),
    ("dont_write_bytecode", "Don't write .pyc files (-B)"),
]

# Console modes for Windows
CONSOLE_MODES = [
    ("Auto", "auto"),
    ("Force Console", "force"),
    ("Disable Console", "disable"),
    ("Attach to Parent", "attach"),
]

# Onefile temp directory modes
ONEFILE_TEMP_MODES = [
    ("Auto", "auto"),
    ("Temporary", "temporary"),
    ("Cached", "cached"),
]

# File reference choices
FILE_REFERENCE_CHOICES = [
    ("Runtime", "runtime"),
    ("Original", "original"),
    ("Frozen", "frozen"),
]

# Progress bar modes
PROGRESS_BAR_MODES = [
    ("Auto", "auto"),
    ("tqdm", "tqdm"),
    ("rich", "rich"),
    ("None", "none"),
]

# Common Nuitka plugins
COMMON_PLUGINS = [
    ("anti-bloat", "Removes unnecessary imports from popular packages"),
    ("tk-inter", "Support for Tkinter applications"),
    ("numpy", "NumPy package support"),
    ("matplotlib", "Matplotlib plotting library support"),
    ("pyqt5", "PyQt5 GUI framework support"),
    ("pyqt6", "PyQt6 GUI framework support"),
    ("pyside2", "PySide2 GUI framework support"),
    ("pyside6", "PySide6 GUI framework support"),
    ("multiprocessing", "Multiprocessing module support"),
    ("pmw-freezer", "Python MegaWidgets support"),
    ("pylint-warnings", "Pylint integration"),
    ("implicit-imports", "Auto-detect implicit imports"),
]

# Anti-bloat options
ANTI_BLOAT_OPTIONS = {
    "setuptools": [("Allow", "allow"), ("Error", "error"), ("Warning", "warning"), ("Ignore", "ignore")],
    "pytest": [("Allow", "allow"), ("Error", "error"), ("Warning", "warning"), ("Ignore", "ignore")],
    "unittest": [("Allow", "allow"), ("Error", "error"), ("Warning", "warning"), ("Ignore", "ignore")],
    "IPython": [("Allow", "allow"), ("Error", "error"), ("Warning", "warning"), ("Ignore", "ignore")],
}

# Window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600

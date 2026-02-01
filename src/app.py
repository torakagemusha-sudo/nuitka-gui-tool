"""
Main application class for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, QDialog, QVBoxLayout,
    QHBoxLayout, QPlainTextEdit, QPushButton, QApplication
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction
from pathlib import Path
import webbrowser

from .core.config import ConfigManager
from .core.command_builder import CommandBuilder
from .core.executor import CompilationExecutor, CompilationStatus
from .core.validator import Validator
from .core.platform_detector import PlatformDetector
from .ui.main_window_improved import MainWindow
from .utils.constants import APP_NAME, APP_VERSION


class NuitkaGUI(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize application."""
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(900, 700)

        # Initialize managers
        self.config = ConfigManager()
        self.executor = None

        # Create main window
        self.main_window = MainWindow(self, self.config, self)
        self.setCentralWidget(self.main_window)

        # Create menu bar
        self.create_menu_bar()

        # Check if Nuitka is installed
        self.check_nuitka()

    def create_menu_bar(self):
        """Create application menu bar with keyboard shortcuts."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Configuration", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setToolTip("Create a new configuration (Ctrl+N)")
        new_action.triggered.connect(self.on_new_config)
        file_menu.addAction(new_action)

        open_action = QAction("&Open Configuration...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setToolTip("Open an existing configuration (Ctrl+O)")
        open_action.triggered.connect(self.on_load_config)
        file_menu.addAction(open_action)

        save_action = QAction("&Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setToolTip("Save current configuration (Ctrl+S)")
        save_action.triggered.connect(self.on_save_config)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save Configuration &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setToolTip("Save configuration with new name (Ctrl+Shift+S)")
        save_as_action.triggered.connect(self.on_save_config_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setToolTip("Exit application (Ctrl+Q)")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Build menu
        build_menu = menubar.addMenu("&Build")

        compile_action = QAction("&Build", self)
        compile_action.setShortcut("F5")
        compile_action.setToolTip("Start compilation (F5)")
        compile_action.triggered.connect(self.on_compile)
        build_menu.addAction(compile_action)

        stop_action = QAction("&Stop", self)
        stop_action.setShortcut("Shift+F5")
        stop_action.setToolTip("Stop running compilation (Shift+F5)")
        stop_action.triggered.connect(self.on_cancel_compile)
        build_menu.addAction(stop_action)

        build_menu.addSeparator()

        validate_action = QAction("&Validate Configuration", self)
        validate_action.setShortcut("Ctrl+Shift+V")
        validate_action.setToolTip("Validate configuration (Ctrl+Shift+V)")
        validate_action.triggered.connect(lambda: self.main_window.validate_placeholder())
        build_menu.addAction(validate_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        show_cmd_action = QAction("Show &Command", self)
        show_cmd_action.setShortcut("Ctrl+K")
        show_cmd_action.setToolTip("Show Nuitka command (Ctrl+K)")
        show_cmd_action.triggered.connect(self.on_show_command)
        view_menu.addAction(show_cmd_action)

        clear_output_action = QAction("C&lear Output", self)
        clear_output_action.setShortcut("Ctrl+L")
        clear_output_action.setToolTip("Clear console output (Ctrl+L)")
        clear_output_action.triggered.connect(self.main_window.clear_output)
        view_menu.addAction(clear_output_action)

        view_menu.addSeparator()

        toggle_theme_action = QAction("Toggle &Theme", self)
        toggle_theme_action.setShortcut("Ctrl+T")
        toggle_theme_action.setToolTip("Switch between light and dark themes (Ctrl+T)")
        toggle_theme_action.triggered.connect(self.main_window.toggle_theme)
        view_menu.addAction(toggle_theme_action)

        toggle_console_action = QAction("Toggle &Console", self)
        toggle_console_action.setShortcut("Ctrl+`")
        toggle_console_action.setToolTip("Show/hide console output (Ctrl+`)")
        toggle_console_action.triggered.connect(lambda: self.main_window.console_dock.setVisible(
            not self.main_window.console_dock.isVisible()
        ))
        view_menu.addAction(toggle_console_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        shortcuts_action = QAction("Keyboard &Shortcuts", self)
        shortcuts_action.setShortcut("F1")
        shortcuts_action.setToolTip("Show all keyboard shortcuts (F1)")
        shortcuts_action.triggered.connect(self.show_shortcuts_dialog)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        about_action = QAction("&About", self)
        about_action.setToolTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        docs_action = QAction("Nuitka &Documentation", self)
        docs_action.setToolTip("Open Nuitka documentation in browser")
        docs_action.triggered.connect(self.open_nuitka_docs)
        help_menu.addAction(docs_action)

    def check_nuitka(self):
        """Check if Nuitka is installed."""
        if not PlatformDetector.has_nuitka():
            QMessageBox.warning(
                self,
                "Nuitka Not Found",
                "Nuitka does not appear to be installed.\n\n"
                "To use this tool, please install Nuitka:\n"
                "pip install nuitka\n\n"
                "You can still configure compilations, but cannot run them."
            )
        else:
            version = PlatformDetector.get_nuitka_version()
            self.main_window.update_status(f"Nuitka {version} detected")

    def on_compile(self):
        """Handle compile button click."""
        # Save current UI values to config
        self.main_window.save_to_config()

        # Validate configuration
        is_valid, messages = Validator.validate_config(self.config)

        if not is_valid or messages:
            message_text = "\n".join(messages)
            if not is_valid:
                QMessageBox.critical(self, "Validation Error", message_text)
                return
            else:
                # Show warnings but allow continuation
                reply = QMessageBox.question(
                    self,
                    "Validation Warnings",
                    message_text + "\n\nContinue anyway?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

        # Build command
        builder = CommandBuilder(self.config)
        command = builder.build()
        command_str = builder.get_command_string()
        self.main_window.set_command_preview(command_str)

        # Show command
        self.main_window.clear_output()
        self.main_window.append_output(f"Command: {command_str}\n\n")

        # Start compilation
        self.executor = CompilationExecutor(
            command,
            output_callback=self.on_compilation_output,
            completion_callback=self.on_compilation_complete
        )

        if self.executor.start():
            self.main_window.set_compiling(True)
            self.main_window.update_status("Compiling...")
        else:
            QMessageBox.critical(self, "Error", "Failed to start compilation")

    def on_cancel_compile(self):
        """Handle cancel compilation."""
        if self.executor and self.executor.is_running():
            reply = QMessageBox.question(
                self,
                "Cancel Compilation",
                "Are you sure you want to cancel the compilation?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.executor.stop()
                self.main_window.append_output("\n\n=== Compilation cancelled by user ===\n")

    def on_compilation_output(self, line):
        """
        Handle compilation output line.

        Args:
            line: Output line from Nuitka
        """
        # This is called from the compilation thread
        # Use QTimer to update UI from main thread
        QTimer.singleShot(0, lambda: self.main_window.append_output(line + "\n"))

    def on_compilation_complete(self, status, return_code):
        """
        Handle compilation completion.

        Args:
            status: CompilationStatus
            return_code: Process return code
        """
        # This is called from the compilation thread
        # Use QTimer to update UI from main thread
        QTimer.singleShot(0, lambda: self._handle_compilation_complete(status, return_code))

    def _handle_compilation_complete(self, status, return_code):
        """Handle compilation completion in main thread."""
        self.main_window.set_compiling(False)

        if status == CompilationStatus.SUCCESS:
            elapsed = self.executor.get_elapsed_time()
            self.main_window.append_output(f"\n\n=== Compilation completed successfully in {elapsed:.1f} seconds ===\n")
            self.main_window.update_status("Compilation successful")
            self.main_window.set_build_result("Success", return_code)
            if self.main_window.current_plan:
                self.main_window.set_last_success_plan(self.main_window.current_plan)
            self.main_window.populate_artifacts()
            QMessageBox.information(self, "Success", "Compilation completed successfully!")
        elif status == CompilationStatus.CANCELLED:
            self.main_window.update_status("Compilation cancelled")
            self.main_window.set_build_result("Cancelled", return_code)
        else:
            self.main_window.append_output(f"\n\n=== Compilation failed with return code {return_code} ===\n")
            self.main_window.update_status("Compilation failed")
            self.main_window.set_build_result("Failed", return_code)
            QMessageBox.critical(self, "Compilation Failed", f"Compilation failed with return code {return_code}")

    def on_new_config(self):
        """Create new configuration."""
        reply = QMessageBox.question(
            self,
            "New Configuration",
            "Create new configuration? Current changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.config.reset()
            self.main_window.load_from_config()
            self.main_window.update_status("New configuration created")

    def on_save_config(self):
        """Save configuration to current file."""
        file_path = self.config.get_file_path()
        if file_path:
            self._save_config_to_file(file_path)
        else:
            self.on_save_config_as()

    def on_save_config_as(self):
        """Save configuration to new file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "JSON files (*.json);;All files (*.*)"
        )
        if file_path:
            self._save_config_to_file(file_path)

    def _save_config_to_file(self, file_path):
        """Save configuration to specified file."""
        # Save current UI values to config
        self.main_window.save_to_config()

        if self.config.save(file_path):
            self.main_window.update_status(f"Configuration saved to {file_path}")
            QMessageBox.information(self, "Success", "Configuration saved successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to save configuration")

    def on_load_config(self):
        """Load configuration from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "JSON files (*.json);;All files (*.*)"
        )
        if file_path:
            if self.config.load(file_path):
                self.main_window.load_from_config()
                self.main_window.update_status(f"Configuration loaded from {file_path}")
                QMessageBox.information(self, "Success", "Configuration loaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to load configuration")

    def on_show_command(self):
        """Show the Nuitka command that would be executed."""
        # Save current UI values to config
        self.main_window.save_to_config()

        # Build command
        builder = CommandBuilder(self.config)
        command_str = builder.get_command_string()

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuitka Command")
        dialog.resize(800, 400)

        # Layout
        layout = QVBoxLayout(dialog)

        # Text widget
        text = QPlainTextEdit(dialog)
        text.setPlainText(command_str)
        text.setReadOnly(True)
        layout.addWidget(text)

        # Button frame
        btn_layout = QHBoxLayout()

        # Copy button
        def copy_to_clipboard():
            clipboard = QApplication.clipboard()
            clipboard.setText(command_str)
            QMessageBox.information(dialog, "Copied", "Command copied to clipboard!")

        copy_btn = QPushButton("Copy to Clipboard", dialog)
        copy_btn.clicked.connect(copy_to_clipboard)
        btn_layout.addWidget(copy_btn)

        btn_layout.addStretch(1)

        close_btn = QPushButton("Close", dialog)
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        dialog.exec()

    def show_shortcuts_dialog(self):
        """Show keyboard shortcuts help dialog."""
        shortcuts_text = (
            "KEYBOARD SHORTCUTS\n"
            "==================\n"
            "\n"
            "File Operations:\n"
            "  Ctrl+N          New Configuration\n"
            "  Ctrl+O          Open Configuration\n"
            "  Ctrl+S          Save Configuration\n"
            "  Ctrl+Shift+S    Save As...\n"
            "  Ctrl+Q          Exit Application\n"
            "\n"
            "Build Operations:\n"
            "  F5              Start Build\n"
            "  Shift+F5        Stop Build\n"
            "  Ctrl+Shift+V    Validate Configuration\n"
            "\n"
            "View:\n"
            "  Ctrl+K          Show Command\n"
            "  Ctrl+L          Clear Output\n"
            "  Ctrl+T          Toggle Theme\n"
            "  Ctrl+`          Toggle Console\n"
            "\n"
            "Help:\n"
            "  F1              Show This Dialog\n"
            "\n"
            "Navigation:\n"
            "  Tab             Navigate between fields\n"
            "  Shift+Tab       Navigate backwards\n"
            "  Enter           Move to next field\n"
            "  Shift+Enter     Move to previous field\n"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Keyboard Shortcuts")
        dialog.setMinimumSize(500, 600)

        layout = QVBoxLayout(dialog)

        text_edit = QPlainTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(shortcuts_text)
        layout.addWidget(text_edit)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setDefault(True)
        layout.addWidget(close_btn)

        dialog.exec()

    def show_about(self):
        """Show about dialog."""
        nuitka_version = PlatformDetector.get_nuitka_version()
        QMessageBox.information(
            self,
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"A GUI wrapper for Nuitka Python Compiler\n\n"
            f"Platform: {PlatformDetector.get_platform()}\n"
            f"{nuitka_version}\n\n"
            f"This tool provides a user-friendly interface for all Nuitka\n"
            f"command-line options, making it easy to compile Python\n"
            f"applications without memorizing flags."
        )

    def open_nuitka_docs(self):
        """Open Nuitka documentation in browser."""
        webbrowser.open("https://nuitka.net/user-documentation/user-manual.html")

    def closeEvent(self, event):
        """Handle window close event."""
        if self.executor and self.executor.is_running():
            QMessageBox.warning(
                self,
                "Compilation Running",
                "Please cancel the compilation before exiting."
            )
            event.ignore()
        else:
            event.accept()

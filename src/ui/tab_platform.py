"""
Platform-specific options tab for Nuitka GUI (PySide6 version).
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QLineEdit,
    QComboBox, QScrollArea, QGroupBox, QFrame
)
from PySide6.QtCore import Qt

from ..core.platform_detector import PlatformDetector
from ..utils.constants import CONSOLE_MODES
from .widgets import FileSelectFrame, add_tooltip


class TabPlatform(QWidget):
    """Tab for platform-specific compilation settings."""

    def __init__(self, parent, config):
        """
        Initialize platform tab.

        Args:
            parent: Parent widget
            config: ConfigManager instance
        """
        super().__init__(parent)
        self.config = config
        self.widgets = {}

        # Create scrollable layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # Content widget
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        self.create_widgets()

        self.content_layout.addStretch(1)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def create_widgets(self):
        """Create widgets for platform tab."""
        # Windows options
        if PlatformDetector.should_show_windows_options():
            self.create_windows_section()

        # macOS options
        if PlatformDetector.should_show_macos_options():
            self.create_macos_section()

        # Linux options
        if PlatformDetector.should_show_linux_options():
            self.create_linux_section()

        # If not on any recognized platform, show message
        if not any([
            PlatformDetector.should_show_windows_options(),
            PlatformDetector.should_show_macos_options(),
            PlatformDetector.should_show_linux_options()
        ]):
            msg_label = QLabel(
                "Platform-specific options will appear here based on your operating system."
            )
            msg_label.setWordWrap(True)
            self.content_layout.addWidget(msg_label)

    def create_windows_section(self):
        """Create Windows-specific options."""
        win_frame = QGroupBox("Windows Options")
        win_layout = QVBoxLayout(win_frame)
        win_layout.setSpacing(8)

        # Icon
        self.widgets['win_icon'] = FileSelectFrame(
            win_frame,
            "Application Icon:",
            mode='file',
            file_types='Icon files (*.ico);;PNG files (*.png);;All files (*.*)'
        )
        add_tooltip(self.widgets['win_icon'], "Icon file for the executable (.ico or .png)")
        win_layout.addWidget(self.widgets['win_icon'])

        # Console mode
        console_frame = QWidget()
        console_layout = QHBoxLayout(console_frame)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(8)

        console_label = QLabel("Console Mode:")
        console_layout.addWidget(console_label)

        self.widgets['console_mode'] = QComboBox()
        self.widgets['console_mode'].addItems([label for label, _ in CONSOLE_MODES])
        self.widgets['console_mode'].setCurrentText('Auto')
        self.widgets['console_mode'].setFixedWidth(150)
        add_tooltip(self.widgets['console_mode'], "Control console window behavior")
        console_layout.addWidget(self.widgets['console_mode'])
        console_layout.addStretch(1)

        win_layout.addWidget(console_frame)

        # UAC options
        self.widgets['uac_admin'] = QCheckBox("Request Administrator privileges (UAC)")
        add_tooltip(self.widgets['uac_admin'], "Request admin rights on startup")
        win_layout.addWidget(self.widgets['uac_admin'])

        # Version information
        version_frame = QGroupBox("Version Information")
        version_layout = QVBoxLayout(version_frame)
        version_layout.setSpacing(8)

        # Product name
        name_frame = QWidget()
        name_layout = QHBoxLayout(name_frame)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(8)

        name_label = QLabel("Product Name:")
        name_label.setFixedWidth(120)
        name_layout.addWidget(name_label)

        self.widgets['product_name'] = QLineEdit()
        name_layout.addWidget(self.widgets['product_name'], 1)

        version_layout.addWidget(name_frame)

        # Product version
        pver_frame = QWidget()
        pver_layout = QHBoxLayout(pver_frame)
        pver_layout.setContentsMargins(0, 0, 0, 0)
        pver_layout.setSpacing(8)

        pver_label = QLabel("Product Version:")
        pver_label.setFixedWidth(120)
        pver_layout.addWidget(pver_label)

        self.widgets['product_version'] = QLineEdit()
        self.widgets['product_version'].setFixedWidth(150)
        add_tooltip(self.widgets['product_version'], "Format: 1.0.0.0 (up to 4 numbers)")
        pver_layout.addWidget(self.widgets['product_version'])
        pver_layout.addStretch(1)

        version_layout.addWidget(pver_frame)

        # File version
        fver_frame = QWidget()
        fver_layout = QHBoxLayout(fver_frame)
        fver_layout.setContentsMargins(0, 0, 0, 0)
        fver_layout.setSpacing(8)

        fver_label = QLabel("File Version:")
        fver_label.setFixedWidth(120)
        fver_layout.addWidget(fver_label)

        self.widgets['file_version'] = QLineEdit()
        self.widgets['file_version'].setFixedWidth(150)
        add_tooltip(self.widgets['file_version'], "Format: 1.0.0.0 (up to 4 numbers)")
        fver_layout.addWidget(self.widgets['file_version'])
        fver_layout.addStretch(1)

        version_layout.addWidget(fver_frame)

        # Company name
        company_frame = QWidget()
        company_layout = QHBoxLayout(company_frame)
        company_layout.setContentsMargins(0, 0, 0, 0)
        company_layout.setSpacing(8)

        company_label = QLabel("Company Name:")
        company_label.setFixedWidth(120)
        company_layout.addWidget(company_label)

        self.widgets['company_name'] = QLineEdit()
        company_layout.addWidget(self.widgets['company_name'], 1)

        version_layout.addWidget(company_frame)

        # Copyright
        copy_frame = QWidget()
        copy_layout = QHBoxLayout(copy_frame)
        copy_layout.setContentsMargins(0, 0, 0, 0)
        copy_layout.setSpacing(8)

        copy_label = QLabel("Copyright:")
        copy_label.setFixedWidth(120)
        copy_layout.addWidget(copy_label)

        self.widgets['copyright'] = QLineEdit()
        copy_layout.addWidget(self.widgets['copyright'], 1)

        version_layout.addWidget(copy_frame)

        win_layout.addWidget(version_frame)

        self.content_layout.addWidget(win_frame)

    def create_macos_section(self):
        """Create macOS-specific options."""
        mac_frame = QGroupBox("macOS Options")
        mac_layout = QVBoxLayout(mac_frame)
        mac_layout.setSpacing(8)

        # Create app bundle
        self.widgets['create_bundle'] = QCheckBox("Create application bundle (.app)")
        add_tooltip(self.widgets['create_bundle'], "Create macOS .app bundle structure")
        mac_layout.addWidget(self.widgets['create_bundle'])

        # Icon
        self.widgets['mac_icon'] = FileSelectFrame(
            mac_frame,
            "Application Icon:",
            mode='file',
            file_types='Icon files (*.icns);;PNG files (*.png);;All files (*.*)'
        )
        add_tooltip(self.widgets['mac_icon'], "Icon file for the application (.icns or .png)")
        mac_layout.addWidget(self.widgets['mac_icon'])

        # App name
        name_frame = QWidget()
        name_layout = QHBoxLayout(name_frame)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(8)

        name_label = QLabel("App Name:")
        name_label.setFixedWidth(100)
        name_layout.addWidget(name_label)

        self.widgets['app_name'] = QLineEdit()
        name_layout.addWidget(self.widgets['app_name'], 1)

        mac_layout.addWidget(name_frame)

        # Bundle ID
        bundle_frame = QWidget()
        bundle_layout = QHBoxLayout(bundle_frame)
        bundle_layout.setContentsMargins(0, 0, 0, 0)
        bundle_layout.setSpacing(8)

        bundle_label = QLabel("Bundle ID:")
        bundle_label.setFixedWidth(100)
        bundle_layout.addWidget(bundle_label)

        self.widgets['bundle_id'] = QLineEdit()
        add_tooltip(self.widgets['bundle_id'], "Format: com.company.appname")
        bundle_layout.addWidget(self.widgets['bundle_id'], 1)

        mac_layout.addWidget(bundle_frame)

        self.content_layout.addWidget(mac_frame)

    def create_linux_section(self):
        """Create Linux-specific options."""
        linux_frame = QGroupBox("Linux Options")
        linux_layout = QVBoxLayout(linux_frame)
        linux_layout.setSpacing(8)

        # Icon
        self.widgets['linux_icon'] = FileSelectFrame(
            linux_frame,
            "Application Icon:",
            mode='file',
            file_types='PNG files (*.png);;All files (*.*)'
        )
        add_tooltip(self.widgets['linux_icon'], "Icon file for the application (.png)")
        linux_layout.addWidget(self.widgets['linux_icon'])

        self.content_layout.addWidget(linux_frame)

    def load_from_config(self):
        """Load values from config."""
        # Windows
        if PlatformDetector.should_show_windows_options():
            self.widgets['win_icon'].set_path(
                self.config.get('platform.windows.icon', '')
            )

            console_mode = self.config.get('platform.windows.console_mode', 'auto')
            # Map console_mode value to label
            for label, value in CONSOLE_MODES:
                if value == console_mode:
                    self.widgets['console_mode'].setCurrentText(label)
                    break

            self.widgets['uac_admin'].setChecked(
                self.config.get('platform.windows.uac_admin', False)
            )

            self.widgets['product_name'].setText(
                self.config.get('platform.windows.product_name', '')
            )
            self.widgets['product_version'].setText(
                self.config.get('platform.windows.product_version', '')
            )
            self.widgets['file_version'].setText(
                self.config.get('platform.windows.file_version', '')
            )
            self.widgets['company_name'].setText(
                self.config.get('platform.windows.company_name', '')
            )
            self.widgets['copyright'].setText(
                self.config.get('platform.windows.copyright', '')
            )

        # macOS
        if PlatformDetector.should_show_macos_options():
            self.widgets['create_bundle'].setChecked(
                self.config.get('platform.macos.create_bundle', False)
            )
            self.widgets['mac_icon'].set_path(
                self.config.get('platform.macos.icon', '')
            )
            self.widgets['app_name'].setText(
                self.config.get('platform.macos.app_name', '')
            )
            self.widgets['bundle_id'].setText(
                self.config.get('platform.macos.bundle_id', '')
            )

        # Linux
        if PlatformDetector.should_show_linux_options():
            self.widgets['linux_icon'].set_path(
                self.config.get('platform.linux.icon', '')
            )

    def save_to_config(self):
        """Save values to config."""
        # Windows
        if PlatformDetector.should_show_windows_options():
            self.config.set('platform.windows.icon', self.widgets['win_icon'].get_path())

            # Map console mode label back to value
            console_label = self.widgets['console_mode'].currentText()
            for label, value in CONSOLE_MODES:
                if label == console_label:
                    self.config.set('platform.windows.console_mode', value)
                    break

            self.config.set('platform.windows.uac_admin', self.widgets['uac_admin'].isChecked())
            self.config.set('platform.windows.product_name', self.widgets['product_name'].text())
            self.config.set('platform.windows.product_version', self.widgets['product_version'].text())
            self.config.set('platform.windows.file_version', self.widgets['file_version'].text())
            self.config.set('platform.windows.company_name', self.widgets['company_name'].text())
            self.config.set('platform.windows.copyright', self.widgets['copyright'].text())

        # macOS
        if PlatformDetector.should_show_macos_options():
            self.config.set('platform.macos.create_bundle', self.widgets['create_bundle'].isChecked())
            self.config.set('platform.macos.icon', self.widgets['mac_icon'].get_path())
            self.config.set('platform.macos.app_name', self.widgets['app_name'].text())
            self.config.set('platform.macos.bundle_id', self.widgets['bundle_id'].text())

        # Linux
        if PlatformDetector.should_show_linux_options():
            self.config.set('platform.linux.icon', self.widgets['linux_icon'].get_path())

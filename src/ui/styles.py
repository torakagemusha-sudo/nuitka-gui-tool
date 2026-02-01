"""
Industrial instrument panel stylesheet for PySide6 Nuitka GUI
"""

# Color Palette - Industrial Warm Light Theme (WCAG AA Compliant)
COLORS_LIGHT = {
    "accent": "#D07A2D",
    "accent_hover": "#B5661E",
    "accent_pressed": "#8E4E16",
    "success": "#3A7C3A",
    "error": "#B23A3A",
    "warning": "#C27A2A",
    "info": "#3B5C8A",
    "background_top": "#F4F0E8",
    "background_bottom": "#E6DED2",
    "card": "#FBFAF7",
    "border": "#D4C9B8",
    "border_hover": "#C5B8A6",
    "text_primary": "#2B2A27",
    "text_secondary": "#4A4640",
    "text_tertiary": "#8B8578",
    "text_disabled": "#767169",
    # Interactive state colors
    "hover_bg": "#F1ECE3",
    "pressed_bg": "#E2DBCF",
    "disabled_bg": "#F5F1EA",
    "ghost_hover_bg": "#F5EFE6",
    "list_hover_bg": "#F3EEE6",
    "inspector_bg": "#F7F2E9",
    "impact_bg": "#E8E0D3",
    "pill_bg": "#EFE6D8",
    "console_border": "#2A2724",
    "expert": "#5B4E90",
    # Console colors
    "console_bg": "#1C1B19",
    "console_fg": "#E6E0D6",
}

# Color Palette - Industrial Warm Dark Theme (WCAG AA Compliant)
COLORS_DARK = {
    "accent": "#E88D3F",  # Lighter for dark backgrounds
    "accent_hover": "#F5A864",
    "accent_pressed": "#D07A2D",
    "success": "#5CB85C",  # Lighter green
    "error": "#E74C3C",    # Lighter red
    "warning": "#F39C12",  # Lighter orange
    "info": "#5DADE2",     # Lighter blue
    # Background layers (darkest to lightest)
    "background_top": "#1C1B19",
    "background_bottom": "#252321",
    "card": "#2B2926",
    "border": "#3D3935",
    "border_hover": "#4D4840",
    # Text colors (14:1, 7:1, 4.5:1, 3:1 contrast ratios)
    "text_primary": "#E6E0D6",
    "text_secondary": "#B5AFA3",
    "text_tertiary": "#8B8578",
    "text_disabled": "#6B6560",
    # Interactive state colors
    "hover_bg": "#353230",
    "pressed_bg": "#3F3C39",
    "disabled_bg": "#2E2C29",
    "ghost_hover_bg": "#353230",
    "list_hover_bg": "#353230",
    "inspector_bg": "#322F2C",
    "impact_bg": "#3D3935",
    "pill_bg": "#3D3935",
    "console_border": "#0E0D0C",
    "expert": "#7B6EB0",
    # Console colors
    "console_bg": "#141312",
    "console_fg": "#E6E0D6",
}

# Default theme
COLORS = COLORS_LIGHT

# Spacing constants
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
}

# Typography (WCAG AA Compliant Font Sizes)
FONTS = {
    "ui": '"Bahnschrift", "Aptos", "DIN Alternate", "Segoe UI", sans-serif',
    "code": '"Cascadia Mono", "Consolas", "SF Mono", monospace',
}

# Font sizes (in points) - WCAG AA compliant
FONT_SIZES = {
    "xs": "9pt",   # Captions, labels (minimum for non-essential text)
    "sm": "10pt",  # Helper text
    "base": "11pt",  # Body text (NEW BASELINE for accessibility)
    "md": "12pt",  # Section text
    "lg": "14pt",  # Headers
    "xl": "16pt",  # Page titles
    "2xl": "20pt",  # App name
}


class ThemeManager:
    """Manages application themes and stylesheet generation."""

    def __init__(self):
        self.current_theme = "light"
        self._observers = []

    def get_colors(self, theme_name="light"):
        """Get color palette for specified theme."""
        if theme_name == "dark":
            return COLORS_DARK
        return COLORS_LIGHT

    def build_stylesheet(self, theme_name="light"):
        """Build complete QSS stylesheet for specified theme."""
        colors = self.get_colors(theme_name)
        return self._generate_qss(colors)

    def switch_theme(self, app, theme_name):
        """Switch application theme."""
        if theme_name not in ["light", "dark"]:
            theme_name = "light"

        self.current_theme = theme_name
        stylesheet = self.build_stylesheet(theme_name)
        app.setStyleSheet(stylesheet)

        # Notify observers
        self._notify_observers(theme_name)

    def add_observer(self, callback):
        """Add theme change observer."""
        self._observers.append(callback)

    def _notify_observers(self, theme_name):
        """Notify all observers of theme change."""
        for callback in self._observers:
            callback(theme_name)

    def _generate_qss(self, colors):
        """Generate QSS stylesheet with given color palette."""
        return f"""
/* ============================= GLOBAL ============================= */
QMainWindow {{
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 {colors['background_top']},
        stop: 1 {colors['background_bottom']}
    );
}}

QWidget {{
    font-family: {FONTS['ui']};
    font-size: {FONT_SIZES['base']};  /* Updated to 11pt for WCAG AA */
    color: {colors['text_primary']};
    background-color: transparent;
}}

/* ============================= PANELS ============================= */
QFrame {{
    border: none;
    background-color: transparent;
}}

QFrame[class="topbar"],
QFrame[class="statusstrip"],
QFrame[class="leftnav"],
QFrame[class="workspace"],
QFrame[class="inspector"],
QFrame[class="dock"] {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
}}

.card {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    padding: 8px;
}}

/* ============================= LABELS ============================= */
QLabel {{
    background-color: transparent;
    color: {colors['text_primary']};
}}

QLabel[class="appname"] {{
    font-size: {FONT_SIZES['xl']};  /* 16pt */
    font-weight: 700;
    letter-spacing: 0.5px;
}}

QLabel[class="muted"] {{
    color: {colors['text_secondary']};
    font-size: {FONT_SIZES['xs']};  /* 9pt - minimum for non-essential text */
}}

QLabel[class="sectiontitle"] {{
    font-size: {FONT_SIZES['md']};  /* 12pt */
    font-weight: 600;
}}

QLabel[class="status"] {{
    font-size: {FONT_SIZES['base']};  /* 11pt */
    font-weight: 600;
}}

QLabel[class="pill"] {{
    background-color: {colors['pill_bg']};
    border: 1px solid {colors['border']};
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 8pt;
}}

QLabel[class="risk"] {{
    border-radius: 8px;
    padding: 2px 6px;
    font-size: 8pt;
    font-weight: 600;
    color: white;
}}

QLabel[class="risk"][risk="safe"] {{
    background-color: {colors['success']};
}}

QLabel[class="risk"][risk="caution"] {{
    background-color: {colors['warning']};
}}

QLabel[class="risk"][risk="risky"] {{
    background-color: {colors['error']};
}}

QLabel[class="risk"][risk="expert"] {{
    background-color: {colors['expert']};
}}

QLabel[class="impact"] {{
    background-color: {colors['impact_bg']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    padding: 2px 6px;
    font-size: 8pt;
}}

/* ============================= BUTTONS ============================= */
QPushButton {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 14px;
    min-height: 24px;
    color: {colors['text_primary']};
}}

QPushButton:hover {{
    background-color: {colors['hover_bg']};
    border-color: {colors['border_hover']};
}}

QPushButton:pressed {{
    background-color: {colors['pressed_bg']};
}}

QPushButton:disabled {{
    background-color: {colors['disabled_bg']};
    color: {colors['text_disabled']};
    border-color: {colors['border']};
}}

QPushButton:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}}

QPushButton[class="primary"] {{
    background-color: {colors['accent']};
    color: white;
    border: none;
    font-weight: 600;
}}

QPushButton[class="primary"]:hover {{
    background-color: {colors['accent_hover']};
}}

QPushButton[class="primary"]:pressed {{
    background-color: {colors['accent_pressed']};
}}

QPushButton[class="ghost"] {{
    background-color: transparent;
    border: 1px solid transparent;
    padding: 4px 10px;
}}

QPushButton[class="ghost"]:hover {{
    background-color: {colors['ghost_hover_bg']};
    border-color: {colors['border']};
}}

QToolButton {{
    background-color: transparent;
    border: 1px solid transparent;
    padding: 4px 8px;
}}

QToolButton:hover {{
    background-color: {colors['ghost_hover_bg']};
    border-color: {colors['border']};
}}

/* ============================= INPUT FIELDS ============================= */
QLineEdit {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 8px;
    min-height: 24px;
    selection-background-color: {colors['accent']};
    selection-color: white;
}}

QLineEdit:hover {{
    border-color: {colors['border_hover']};
}}

QLineEdit:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
    padding: 5px 7px;
}}

QComboBox {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 6px 8px;
    min-height: 24px;
}}

QComboBox:hover {{
    border-color: {colors['border_hover']};
}}

QComboBox:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: none;
    border: 4px solid transparent;
    border-top-color: {colors['text_secondary']};
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    selection-background-color: {colors['accent']};
    selection-color: white;
    outline: none;
}}

/* ============================= LIST WIDGET ============================= */
QListWidget {{
    background-color: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    outline: none;
    padding: 4px;
}}

QListWidget::item {{
    padding: 6px 8px;
    border-radius: 4px;
}}

QListWidget::item:hover {{
    background-color: {colors['list_hover_bg']};
}}

QListWidget::item:selected {{
    background-color: {colors['accent']};
    color: white;
}}

QListWidget::item:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
}}

QListWidget:focus {{
    border: 2px solid {colors['accent']};
}}

/* ============================= TABS ============================= */
QTabWidget::pane {{
    border: 1px solid {colors['border']};
    border-radius: 6px;
    background-color: {colors['card']};
}}

QTabBar::tab {{
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 8px 14px;
    min-width: 80px;
    color: {colors['text_secondary']};
    font-weight: 600;
}}

QTabBar::tab:selected {{
    color: {colors['accent']};
    border-bottom-color: {colors['accent']};
}}

QTabBar::tab:hover {{
    color: {colors['text_primary']};
    background-color: {colors['list_hover_bg']};
}}

/* ============================= TEXT EDITS ============================= */
QPlainTextEdit {{
    background-color: {colors['card']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    padding: 8px;
    font-family: {FONTS['code']};
    font-size: 9pt;
}}

QPlainTextEdit[class="console"] {{
    background-color: {colors['console_bg']};
    color: {colors['console_fg']};
    border: 1px solid {colors['console_border']};
}}

QPlainTextEdit[class="inspectorbody"] {{
    background-color: {colors['inspector_bg']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
}}

/* ============================= SCROLL BAR ============================= */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {colors['border']};
    min-height: 30px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors['border_hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QSplitter::handle {{
    background-color: {colors['border']};
}}

QSplitter::handle:hover {{
    background-color: {colors['accent']};
}}

QToolTip {{
    background-color: {colors['console_bg']};
    color: {colors['console_fg']};
    border: 1px solid {colors['console_border']};
    border-radius: 6px;
    padding: 6px 8px;
    font-size: {FONT_SIZES['xs']};
}}

/* ============================= ACCESSIBILITY ============================= */
/* Enhanced focus indicators for WCAG AA compliance */

QCheckBox:focus, QRadioButton:focus {{
    outline: 2px solid {colors['accent']};
    outline-offset: 4px;
}}

QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {colors['accent']};
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}}

/* Ensure all interactive elements have visible focus */
*:focus {{
    outline: 2px solid {colors['accent']};
    outline-offset: 2px;
}}

/* Typography utility classes */
.text-xs {{ font-size: {FONT_SIZES['xs']}; }}
.text-sm {{ font-size: {FONT_SIZES['sm']}; }}
.text-base {{ font-size: {FONT_SIZES['base']}; }}
.text-md {{ font-size: {FONT_SIZES['md']}; }}
.text-lg {{ font-size: {FONT_SIZES['lg']}; }}
.text-xl {{ font-size: {FONT_SIZES['xl']}; }}
.text-2xl {{ font-size: {FONT_SIZES['2xl']}; }}
"""


# Global theme manager instance
theme_manager = ThemeManager()


def apply_stylesheet(app, theme="light"):
    """
    Apply the stylesheet to the application.

    Args:
        app: QApplication instance
        theme: Theme name ("light" or "dark")
    """
    theme_manager.switch_theme(app, theme)

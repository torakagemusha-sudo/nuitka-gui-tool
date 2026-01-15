"""
Industrial instrument panel stylesheet for PySide6 Nuitka GUI
"""
# Color Palette - Industrial Warm
COLORS = {
    "accent": "#D07A2D",
    "accent_hover": "#B5661E",
    "accent_pressed": "#8E4E16",
    "success": "#3A7C3A",
    "error": "#B23A3A",
    "warning": "#C27A2A",
    "background_top": "#F4F0E8",
    "background_bottom": "#E6DED2",
    "card": "#FBFAF7",
    "border": "#D4C9B8",
    "text_primary": "#2B2A27",
    "text_secondary": "#5E5A52",
    "text_disabled": "#9B9488",
    "dark_bg": "#1C1B19",
    "dark_fg": "#E6E0D6",
}

# Spacing constants
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
}

# Typography
FONTS = {
    "ui": '"Bahnschrift", "Aptos", "DIN Alternate", "Segoe UI", sans-serif',
    "code": '"Cascadia Mono", "Consolas", "SF Mono", monospace',
}

FLUENT_QSS = f"""
/* ============================= GLOBAL ============================= */
QMainWindow {{
    background-color: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 {COLORS['background_top']},
        stop: 1 {COLORS['background_bottom']}
    );
}}

QWidget {{
    font-family: {FONTS['ui']};
    font-size: 9pt;
    color: {COLORS['text_primary']};
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
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
}}

.card {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
}}

/* ============================= LABELS ============================= */
QLabel {{
    background-color: transparent;
    color: {COLORS['text_primary']};
}}

QLabel[class="appname"] {{
    font-size: 12pt;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

QLabel[class="muted"] {{
    color: {COLORS['text_secondary']};
    font-size: 8pt;
}}

QLabel[class="sectiontitle"] {{
    font-size: 10pt;
    font-weight: 600;
}}

QLabel[class="status"] {{
    font-size: 9pt;
    font-weight: 600;
}}

QLabel[class="pill"] {{
    background-color: #EFE6D8;
    border: 1px solid {COLORS['border']};
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
    background-color: #3A7C3A;
}}

QLabel[class="risk"][risk="caution"] {{
    background-color: #C27A2A;
}}

QLabel[class="risk"][risk="risky"] {{
    background-color: #B23A3A;
}}

QLabel[class="risk"][risk="expert"] {{
    background-color: #5B4E90;
}}

QLabel[class="impact"] {{
    background-color: #E8E0D3;
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 2px 6px;
    font-size: 8pt;
}}

/* ============================= BUTTONS ============================= */
QPushButton {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 14px;
    min-height: 24px;
    color: {COLORS['text_primary']};
}}

QPushButton:hover {{
    background-color: #F1ECE3;
    border-color: #C5B8A6;
}}

QPushButton:pressed {{
    background-color: #E2DBCF;
}}

QPushButton:disabled {{
    background-color: #F5F1EA;
    color: {COLORS['text_disabled']};
    border-color: {COLORS['border']};
}}

QPushButton[class="primary"] {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
    font-weight: 600;
}}

QPushButton[class="primary"]:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton[class="primary"]:pressed {{
    background-color: {COLORS['accent_pressed']};
}}

QPushButton[class="ghost"] {{
    background-color: transparent;
    border: 1px solid transparent;
    padding: 4px 10px;
}}

QPushButton[class="ghost"]:hover {{
    background-color: #F5EFE6;
    border-color: #D4C9B8;
}}

QToolButton {{
    background-color: transparent;
    border: 1px solid transparent;
    padding: 4px 8px;
}}

QToolButton:hover {{
    background-color: #F5EFE6;
    border-color: #D4C9B8;
}}

/* ============================= INPUT FIELDS ============================= */
QLineEdit {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 8px;
    min-height: 24px;
    selection-background-color: {COLORS['accent']};
    selection-color: white;
}}

QLineEdit:hover {{
    border-color: #C5B8A6;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['accent']};
    padding: 5px 7px;
}}

QComboBox {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 6px 8px;
    min-height: 24px;
}}

QComboBox:hover {{
    border-color: #C5B8A6;
}}

QComboBox:focus {{
    border: 2px solid {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: none;
    border: 4px solid transparent;
    border-top-color: {COLORS['text_secondary']};
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    selection-background-color: {COLORS['accent']};
    selection-color: white;
    outline: none;
}}

/* ============================= LIST WIDGET ============================= */
QListWidget {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    outline: none;
    padding: 4px;
}}

QListWidget::item {{
    padding: 6px 8px;
    border-radius: 4px;
}}

QListWidget::item:hover {{
    background-color: #F3EEE6;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: white;
}}

/* ============================= TABS ============================= */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background-color: {COLORS['card']};
}}

QTabBar::tab {{
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 8px 14px;
    min-width: 80px;
    color: {COLORS['text_secondary']};
    font-weight: 600;
}}

QTabBar::tab:selected {{
    color: {COLORS['accent']};
    border-bottom-color: {COLORS['accent']};
}}

QTabBar::tab:hover {{
    color: {COLORS['text_primary']};
    background-color: #F3EEE6;
}}

/* ============================= TEXT EDITS ============================= */
QPlainTextEdit {{
    background-color: {COLORS['card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px;
    font-family: {FONTS['code']};
    font-size: 9pt;
}}

QPlainTextEdit[class="console"] {{
    background-color: {COLORS['dark_bg']};
    color: {COLORS['dark_fg']};
    border: 1px solid #2A2724;
}}

QPlainTextEdit[class="inspectorbody"] {{
    background-color: #F7F2E9;
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
}}

/* ============================= SCROLL BAR ============================= */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: #C9BDAA;
    min-height: 30px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #B3A691;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QSplitter::handle {{
    background-color: {COLORS['border']};
}}

QSplitter::handle:hover {{
    background-color: {COLORS['accent']};
}}

QToolTip {{
    background-color: {COLORS['dark_bg']};
    color: {COLORS['dark_fg']};
    border: 1px solid #2A2724;
    border-radius: 6px;
    padding: 6px 8px;
    font-size: 8pt;
}}
"""


def apply_stylesheet(app):
    """Apply the stylesheet to the application."""
    app.setStyleSheet(FLUENT_QSS)

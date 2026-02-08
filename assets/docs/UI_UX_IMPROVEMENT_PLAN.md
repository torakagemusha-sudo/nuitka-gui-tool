# UI/UX Improvement Plan for Nuitka GUI Tool

**Version:** 1.0
**Date:** 2026-01-15
**Status:** Planning Phase

---

## Executive Summary

This document outlines a comprehensive plan to transform the Nuitka GUI Tool into a modern, accessible, and user-friendly application. The plan addresses critical accessibility violations, implements dark mode, enhances validation feedback, and modernizes the overall user experience while maintaining the industrial warm aesthetic.

### Key Objectives

1. **Achieve WCAG 2.1 AA Compliance** - Fix color contrast, font sizes, and screen reader support
2. **Implement Dark Mode** - Comprehensive theme system with user preference
3. **Enhance Keyboard Navigation** - Full keyboard accessibility and power user shortcuts
4. **Improve Validation & Feedback** - Real-time validation with clear error messaging
5. **Optimize Information Architecture** - Progressive disclosure and visual hierarchy
6. **Modernize UI Patterns** - Replace modal dialogs with non-blocking notifications

### Current State

- **Framework**: PySide6 (Qt for Python)
- **Architecture**: Data-driven tabs with JSON configuration
- **Theme**: Industrial warm color palette
- **Lines of Code**: ~730 (main window), ~387 (styles), ~370 (widgets)

### Expected Outcomes

- **Accessibility**: 100% WCAG 2.1 AA compliance
- **User Satisfaction**: 30% reduction in task completion time
- **Error Reduction**: 50% fewer validation errors through real-time feedback
- **Dark Mode Adoption**: 40%+ of users switching to dark theme

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Phase 1: Accessibility Foundation](#phase-1-accessibility-foundation-week-1-2)
3. [Phase 2: Dark Mode Implementation](#phase-2-dark-mode-implementation-week-2-3)
4. [Phase 3: Keyboard Navigation & Shortcuts](#phase-3-keyboard-navigation--shortcuts-week-3-4)
5. [Phase 4: Validation & Error Feedback](#phase-4-validation--error-feedback-week-4-5)
6. [Phase 5: Visual Hierarchy & Information Density](#phase-5-visual-hierarchy--information-density-week-5-6)
7. [Phase 6: Modern UI Patterns](#phase-6-modern-ui-patterns-week-6-7)
8. [Phase 7: Polish & Performance](#phase-7-polish--performance-week-7-8)
9. [Phase 8: Documentation & Testing](#phase-8-documentation--testing-week-8)
10. [Implementation Priority Matrix](#implementation-priority-matrix)
11. [Success Metrics](#success-metrics)

---

## Current State Analysis

### Architecture Overview

**Key Files:**
- `src/ui/main_window_improved.py` (730 lines) - Main UI structure
- `src/ui/styles.py` (387 lines) - Styling and themes
- `src/ui/widgets.py` (370 lines) - Custom widgets
- `src/ui/tab_data_driven.py` (349 lines) - Generic tab system
- `src/core/validator.py` (246 lines) - Validation framework
- `configs/setting_definitions.json` - Data-driven settings

### Strengths

✅ **Modern Architecture**
- PySide6 framework with signal/slot pattern
- Data-driven configuration from JSON
- Comprehensive QSS stylesheet (381 lines)
- Good widget abstraction and reusability

✅ **Visual Design**
- Industrial warm color palette with brand identity
- Consistent spacing system (xs/sm/md/lg/xl)
- Risk-aware UI with visual indicators
- Smooth animations (200ms with InOutCubic easing)

✅ **Feature Completeness**
- Real-time compilation output
- Command preview
- Configuration save/load
- Preset system

### Critical Issues

❌ **Accessibility Violations**
- Color contrast failures (text_secondary: ~3.5:1, needs 4.5:1)
- Font sizes too small (9pt base, needs 11pt minimum)
- No screen reader support (missing ARIA labels)
- No keyboard focus indicators
- No keyboard shortcuts documented

❌ **Inconsistent UX**
- Only input file has real-time validation
- Modal dialogs block workflow
- No error navigation (can't jump to problematic fields)
- No inline error messages (just ✗ without explanation)

❌ **Missing Modern Features**
- Dark mode defined but not implemented
- No theme switching UI
- No toast notifications (uses modal dialogs)
- No drag & drop support
- No command palette

❌ **Information Architecture**
- Status bar overcrowded (6 pieces of information)
- No progressive disclosure (all options visible)
- Inconsistent styling across tabs (some use emojis, some don't)
- No minimum panel widths (can resize to unusable sizes)

---

## Phase 1: Accessibility Foundation (Week 1-2)

**Goal**: Achieve WCAG 2.1 AA compliance basics
**Priority**: Critical
**Complexity**: Medium

### 1.1 Color Contrast Improvements

**File**: `src/ui/styles.py`
**Complexity**: Simple
**Time Estimate**: 4 hours

**Current Issues:**
```python
COLORS = {
    "text_secondary": "#5E5A52",  # ~3.5:1 on #FBFAF7 (FAILS)
    "text_disabled": "#9B9488",   # ~2.5:1 on #FBFAF7 (FAILS)
}
```

**Solution:**
Update color values to meet WCAG AA requirements:
```python
COLORS = {
    "text_secondary": "#4A4640",  # 4.5:1+ contrast
    "text_disabled": "#767169",   # 3:1+ contrast (large text)
    "text_tertiary": "#8B8578",   # For less important text
}
```

**Testing**:
- Use WebAIM Contrast Checker for all text/background combinations
- Verify on actual displays (not just tools)
- Test with reduced saturation to simulate color blindness

**Acceptance Criteria:**
- [ ] All text has 4.5:1 minimum contrast ratio
- [ ] Large text (14pt+) has 3:1 minimum contrast
- [ ] UI components have 3:1 minimum contrast with backgrounds

---

### 1.2 Font Size Accessibility

**File**: `src/ui/styles.py`
**Complexity**: Simple
**Time Estimate**: 3 hours

**Current Issues:**
```python
QWidget {
    font-size: 9pt;  # Too small for accessibility
}
```

**Solution:**
Increase base font size and create proper typography scale:
```python
# Font sizes (in points)
FONT_SIZES = {
    "xs": 9,   # Captions, labels
    "sm": 10,  # Helper text
    "base": 11,  # Body text (NEW BASELINE)
    "md": 12,  # Section text
    "lg": 14,  # Headers
    "xl": 16,  # Page titles
    "2xl": 20,  # App name
}

QWidget {
    font-size: 11pt;  # New baseline
}
```

**Testing**:
- Test with Windows Display Scaling (125%, 150%, 200%)
- Verify readability at arm's length (~28 inches)
- Test on high-DPI displays

**Acceptance Criteria:**
- [ ] Base font size is 11pt minimum
- [ ] Typography scale is consistent across all tabs
- [ ] Text remains readable at 200% zoom

---

### 1.3 ARIA Labels and Screen Reader Support

**Files**: `src/ui/widgets.py`, `src/ui/tab_data_driven.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Current Issues:**
- No accessible names or descriptions
- Labels not associated with controls
- Custom widgets have no ARIA roles
- No state announcements (expanded/collapsed, loading, etc.)

**Solution:**

**In `src/ui/widgets.py`:**
```python
class FileSelectFrame(QFrame):
    def __init__(self, ...):
        # Add accessible names
        self.entry.setAccessibleName(f"{label_text} file path")
        self.entry.setAccessibleDescription("Enter or browse for a file")
        self.browse_btn.setAccessibleName(f"Browse for {label_text}")
        self.browse_btn.setAccessibleDescription("Open file dialog")

class ListBoxWithButtons(QWidget):
    def __init__(self, ...):
        self.listbox.setAccessibleName(label_text)
        self.listbox.setAccessibleDescription(f"List of {label_text.lower()}")
        self.add_btn.setAccessibleName(f"Add {label_text}")
        self.remove_btn.setAccessibleName(f"Remove selected {label_text}")
```

**In `src/ui/tab_data_driven.py`:**
```python
def _create_control(self, setting):
    """Create control with proper accessibility."""
    widget = # ... create widget

    # Add accessible labels
    label_text = setting.get("label", "")
    description = setting.get("description", "")

    widget.setAccessibleName(label_text)
    if description:
        widget.setAccessibleDescription(description)

    return widget
```

**Testing**:
- NVDA (Windows) - Navigate through all controls
- JAWS (Windows) - Verify all labels are announced
- VoiceOver (macOS) - Test navigation and announcements
- Orca (Linux) - Verify basic functionality

**Acceptance Criteria:**
- [ ] All interactive widgets have accessible names
- [ ] Form labels are properly associated with controls
- [ ] Custom widgets announce their state
- [ ] Screen reader can navigate entire application
- [ ] Dynamic content changes are announced

---

### 1.4 Focus Indicators

**File**: `src/ui/styles.py`
**Complexity**: Simple
**Time Estimate**: 4 hours

**Current Issues:**
- No visible focus indicators
- Can't tell which element has keyboard focus
- Default Qt focus is often too subtle

**Solution:**
Add prominent focus styles to QSS:
```css
/* Focus indicators for all interactive elements */
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #D07A2D;
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}

QComboBox:focus {
    border: 2px solid #D07A2D;
    outline: 2px solid rgba(208, 122, 45, 0.3);
}

QPushButton:focus {
    border: 2px solid #D07A2D;
    outline: 2px solid rgba(208, 122, 45, 0.3);
    outline-offset: 2px;
}

QCheckBox:focus, QRadioButton:focus {
    outline: 2px solid #D07A2D;
    outline-offset: 4px;
}

/* Tab focus */
QListWidget::item:focus {
    border: 2px solid #D07A2D;
    background-color: rgba(208, 122, 45, 0.1);
}
```

**Testing**:
- Tab through entire application
- Verify focus is always visible
- Test in different themes (light/dark)
- Test with high contrast mode

**Acceptance Criteria:**
- [ ] All focusable elements have 2px+ visible focus indicator
- [ ] Focus indicator uses accent color (#D07A2D)
- [ ] Focus order is logical and follows visual layout
- [ ] Focus remains visible when keyboard navigating

---

## Phase 2: Dark Mode Implementation (Week 2-3)

**Goal**: Comprehensive dark theme support
**Priority**: High
**Complexity**: Medium

### 2.1 Dark Color Palette

**File**: `src/ui/styles.py`
**Complexity**: Medium
**Time Estimate**: 6 hours

**Current State:**
Colors are defined but unused:
```python
"dark_bg": "#1C1B19",
"dark_fg": "#E6E0D6",
```

**Solution:**
Create complete dark color palette:
```python
DARK_COLORS = {
    # Primary colors
    "accent": "#E88D3F",  # Lighter for dark backgrounds
    "accent_hover": "#F5A864",
    "accent_pressed": "#D07A2D",

    # Status colors
    "success": "#5CB85C",  # Lighter green
    "error": "#E74C3C",    # Lighter red
    "warning": "#F39C12",  # Lighter orange
    "info": "#3498DB",     # Lighter blue

    # Background layers
    "background_top": "#1C1B19",     # Darkest
    "background_bottom": "#252321",  # Slightly lighter
    "card": "#2B2926",              # Elevated surfaces
    "card_hover": "#333028",        # Hover state
    "highlight": "#3A3430",         # Selected/active

    # Borders & dividers
    "border": "#3D3935",
    "border_subtle": "#333028",

    # Text colors
    "text_primary": "#E6E0D6",      # Main text (14:1 contrast)
    "text_secondary": "#B5AFA3",    # Secondary (7:1 contrast)
    "text_tertiary": "#8B8578",     # Tertiary (4.5:1 contrast)
    "text_disabled": "#6B6560",     # Disabled (3:1 contrast)

    # UI elements
    "input_bg": "#252321",
    "input_border": "#3D3935",
    "button_bg": "#333028",
    "button_border": "#3D3935",

    # Console (code)
    "console_bg": "#1C1B19",
    "console_fg": "#E6E0D6",
    "console_output": "#B5AFA3",
    "console_error": "#E74C3C",
    "console_warning": "#F39C12",
    "console_success": "#5CB85C",
}
```

**Testing**:
- Verify all colors meet WCAG AA contrast in dark mode
- Test on OLED displays (true blacks)
- Compare with system dark themes
- Test for eye strain during extended use

**Acceptance Criteria:**
- [ ] Complete dark palette with all UI states
- [ ] All text meets WCAG AA contrast ratios
- [ ] Dark theme matches industrial warm aesthetic
- [ ] Colors look good on different display types

---

### 2.2 Theme Switching System

**Files**: `src/ui/styles.py`, `src/core/config.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Solution:**
Create theme management system:

**File: `src/ui/styles.py`**
```python
class ThemeManager:
    """Manages application themes."""

    def __init__(self):
        self.current_theme = "light"
        self._observers = []

    def get_colors(self, theme_name="light"):
        """Get color palette for theme."""
        if theme_name == "dark":
            return DARK_COLORS
        return COLORS

    def build_stylesheet(self, theme_name="light"):
        """Build complete QSS stylesheet for theme."""
        colors = self.get_colors(theme_name)
        spacing = SPACING
        fonts = FONTS

        # Generate QSS with proper color substitution
        return build_qss(colors, spacing, fonts)

    def switch_theme(self, app, theme_name):
        """Switch application theme."""
        if theme_name not in ["light", "dark"]:
            theme_name = "light"

        self.current_theme = theme_name
        stylesheet = self.build_stylesheet(theme_name)
        app.setStyleSheet(stylesheet)

        # Notify observers
        self._notify_observers(theme_name)

    def detect_system_theme(self):
        """Detect system theme preference."""
        # Qt 6.5+ has QStyleHints.colorScheme()
        from PySide6.QtGui import QGuiApplication
        app = QGuiApplication.instance()
        if hasattr(app.styleHints(), 'colorScheme'):
            from PySide6.QtCore import Qt
            scheme = app.styleHints().colorScheme()
            if scheme == Qt.ColorScheme.Dark:
                return "dark"
        return "light"

    def add_observer(self, callback):
        """Add theme change observer."""
        self._observers.append(callback)

    def _notify_observers(self, theme_name):
        """Notify all observers of theme change."""
        for callback in self._observers:
            callback(theme_name)

# Global theme manager instance
theme_manager = ThemeManager()
```

**File: `src/core/config.py`**
Add theme preference to config:
```python
def _get_default_config(self):
    return {
        "app": {
            "theme": "auto",  # "light", "dark", or "auto"
            "theme_auto_switch": True,
        },
        # ... existing config
    }
```

**Testing**:
- Switch themes multiple times without restart
- Test with system theme changes
- Verify config persistence
- Test on all platforms

**Acceptance Criteria:**
- [ ] Themes switch instantly without restart
- [ ] Theme preference saved to config
- [ ] System theme detection works (Qt 6.5+)
- [ ] No visual glitches during switch
- [ ] All custom widgets update correctly

---

### 2.3 Theme Toggle UI

**File**: `src/ui/main_window_improved.py`
**Complexity**: Simple
**Time Estimate**: 4 hours

**Solution:**
Add theme toggle to header:

```python
# In _create_header() method (around line 106)
def _create_header(self):
    # ... existing code ...

    # Theme toggle button
    self.theme_toggle = QPushButton()
    self.theme_toggle.setProperty("class", "icon-button")
    self.theme_toggle.setFixedSize(32, 32)
    self.theme_toggle.setToolTip("Toggle theme (Ctrl+T)")
    self.theme_toggle.clicked.connect(self.toggle_theme)
    self._update_theme_icon()

    # Add to header
    header_layout.addWidget(self.theme_toggle)

def toggle_theme(self):
    """Toggle between light and dark themes."""
    current = self.app.theme_manager.current_theme
    new_theme = "dark" if current == "light" else "light"

    # Save preference
    self.config.set("app.theme", new_theme)
    self.config.save(self.config.get_file_path())

    # Switch theme
    self.app.theme_manager.switch_theme(self.app, new_theme)
    self._update_theme_icon()

    # Show toast notification
    self.show_toast(f"Switched to {new_theme} theme", "info")

def _update_theme_icon(self):
    """Update theme toggle icon."""
    theme = self.app.theme_manager.current_theme
    icon_text = "☀️" if theme == "dark" else "🌙"
    self.theme_toggle.setText(icon_text)
```

**Also add to View menu:**
```python
# In src/app.py
theme_action = QAction("Toggle Theme", self)
theme_action.setShortcut("Ctrl+T")
theme_action.triggered.connect(self.main_window.toggle_theme)
view_menu.addAction(theme_action)
```

**Testing**:
- Click toggle button
- Use Ctrl+T shortcut
- Verify icon changes
- Test toast notification
- Verify preference persists

**Acceptance Criteria:**
- [ ] Toggle button in header
- [ ] Ctrl+T keyboard shortcut works
- [ ] Icon updates on theme change
- [ ] Toast notification shows
- [ ] Preference saved and loaded correctly

---

### 2.4 Dynamic Theme Updates

**Files**: Various custom widgets
**Complexity**: Medium
**Time Estimate**: 6 hours

**Issue:**
Custom painted widgets (StatusIndicator, etc.) may not update with theme changes.

**Solution:**

**File: `src/ui/main_window_improved.py`**
```python
class StatusIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ... existing code ...

        # Subscribe to theme changes
        from .styles import theme_manager
        theme_manager.add_observer(self._on_theme_change)

    def _on_theme_change(self, theme_name):
        """Handle theme change."""
        # Force repaint with new colors
        self.update()

    def paintEvent(self, event):
        """Paint with theme-aware colors."""
        from .styles import theme_manager
        colors = theme_manager.get_colors()

        # Use colors from current theme
        # ... painting code ...
```

**For all custom painted widgets:**
- Subscribe to theme change notifications
- Trigger repaint on theme change
- Use theme_manager.get_colors() for color lookups
- Test both light and dark themes

**Testing**:
- Switch themes with application open
- Verify all widgets update immediately
- Check for visual glitches
- Test all tab pages

**Acceptance Criteria:**
- [ ] All widgets update on theme change
- [ ] No manual refresh needed
- [ ] Custom painted widgets use theme colors
- [ ] No visual artifacts during transition

---

## Phase 3: Keyboard Navigation & Shortcuts (Week 3-4)

**Goal**: Full keyboard accessibility and power user shortcuts
**Priority**: High
**Complexity**: Medium

### 3.1 Global Keyboard Shortcuts

**File**: `src/app.py`
**Complexity**: Medium
**Time Estimate**: 6 hours

**Current State:**
Basic menu shortcuts exist (Alt+N, Alt+O, Alt+S) but incomplete.

**Solution:**
Comprehensive keyboard shortcut system:

```python
def _create_actions(self):
    """Create all application actions with shortcuts."""

    # File operations
    self.new_action = self._create_action(
        "&New Configuration", "Ctrl+N", self.new_config,
        "Create a new configuration"
    )
    self.open_action = self._create_action(
        "&Open Configuration...", "Ctrl+O", self.open_config,
        "Open an existing configuration"
    )
    self.save_action = self._create_action(
        "&Save Configuration", "Ctrl+S", self.save_config,
        "Save current configuration"
    )
    self.save_as_action = self._create_action(
        "Save &As...", "Ctrl+Shift+S", self.save_config_as,
        "Save configuration with new name"
    )

    # Build operations
    self.build_action = self._create_action(
        "&Build", "F5", self.compile_code,
        "Start compilation"
    )
    self.stop_action = self._create_action(
        "S&top", "Shift+F5", self.stop_compilation,
        "Stop running compilation"
    )
    self.validate_action = self._create_action(
        "&Validate", "Ctrl+Shift+V", self.validate_config,
        "Validate configuration"
    )
    self.show_command_action = self._create_action(
        "Show &Command", "Ctrl+K", self.show_command,
        "Show Nuitka command"
    )

    # View operations
    self.toggle_console_action = self._create_action(
        "Toggle &Console", "Ctrl+`", self.main_window.toggle_console,
        "Show/hide console output"
    )
    self.toggle_theme_action = self._create_action(
        "Toggle &Theme", "Ctrl+T", self.main_window.toggle_theme,
        "Switch between light and dark themes"
    )
    self.search_action = self._create_action(
        "&Find Setting...", "Ctrl+F", self.main_window.focus_search,
        "Search for a setting"
    )

    # Navigation
    self.next_tab_action = self._create_action(
        "Next Tab", "Ctrl+Tab", lambda: self.main_window.next_tab(),
        "Switch to next tab"
    )
    self.prev_tab_action = self._create_action(
        "Previous Tab", "Ctrl+Shift+Tab", lambda: self.main_window.prev_tab(),
        "Switch to previous tab"
    )

    # Tab shortcuts (Alt+1 through Alt+6)
    for i in range(1, 7):
        action = self._create_action(
            f"Tab {i}", f"Alt+{i}",
            lambda idx=i-1: self.main_window.set_current_tab_index(idx),
            f"Switch to tab {i}"
        )
        self.addAction(action)

    # Help
    self.shortcuts_action = self._create_action(
        "Keyboard &Shortcuts", "Ctrl+?", self.show_shortcuts_dialog,
        "Show all keyboard shortcuts"
    )

def _create_action(self, text, shortcut, slot, tooltip):
    """Helper to create action with shortcut."""
    action = QAction(text, self)
    if shortcut:
        action.setShortcut(shortcut)
    action.setToolTip(f"{tooltip} ({shortcut})" if shortcut else tooltip)
    action.triggered.connect(slot)
    return action
```

**Testing**:
- Test all shortcuts
- Verify no conflicts with system shortcuts
- Test on all platforms (shortcuts may differ)
- Verify tooltips show shortcuts

**Acceptance Criteria:**
- [ ] All major actions have keyboard shortcuts
- [ ] F5 builds, Shift+F5 stops
- [ ] Ctrl+F focuses search
- [ ] Alt+1-6 switches tabs
- [ ] Ctrl+Tab cycles tabs
- [ ] All shortcuts work on Windows, macOS, Linux

---

### 3.2 Keyboard Shortcuts Help Dialog

**File**: New file `src/ui/shortcuts_dialog.py`
**Complexity**: Simple
**Time Estimate**: 4 hours

**Solution:**
Create help dialog showing all shortcuts:

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PySide6.QtCore import Qt

class ShortcutsDialog(QDialog):
    """Dialog showing all keyboard shortcuts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)

        # Create table
        table = QTableWidget(self)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Shortcut", "Action"])
        table.horizontalHeader().setStretchLastSection(True)

        # Add shortcuts
        shortcuts = [
            ("File", None),
            ("Ctrl+N", "New Configuration"),
            ("Ctrl+O", "Open Configuration"),
            ("Ctrl+S", "Save Configuration"),
            ("Ctrl+Shift+S", "Save As..."),
            ("", ""),
            ("Build", None),
            ("F5", "Start Build"),
            ("Shift+F5", "Stop Build"),
            ("Ctrl+Shift+V", "Validate Configuration"),
            ("Ctrl+K", "Show Command"),
            ("", ""),
            ("View", None),
            ("Ctrl+F", "Find Setting"),
            ("Ctrl+T", "Toggle Theme"),
            ("Ctrl+`", "Toggle Console"),
            ("", ""),
            ("Navigation", None),
            ("Ctrl+Tab", "Next Tab"),
            ("Ctrl+Shift+Tab", "Previous Tab"),
            ("Alt+1 ... Alt+6", "Jump to Tab"),
            ("", ""),
            ("Help", None),
            ("Ctrl+?", "Show This Dialog"),
        ]

        table.setRowCount(len(shortcuts))
        for i, (shortcut, action) in enumerate(shortcuts):
            shortcut_item = QTableWidgetItem(shortcut)
            action_item = QTableWidgetItem(action or "")

            # Bold section headers
            if action is None:
                font = shortcut_item.font()
                font.setBold(True)
                shortcut_item.setFont(font)

            table.setItem(i, 0, shortcut_item)
            table.setItem(i, 1, action_item)

        table.resizeColumnsToContents()
        layout.addWidget(table)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
```

**Testing**:
- Open with Ctrl+? or F1
- Verify all shortcuts listed
- Test dialog on different screen sizes

**Acceptance Criteria:**
- [ ] Dialog shows all shortcuts organized by category
- [ ] Accessible via Ctrl+? and Help menu
- [ ] Keyboard navigable (Tab, Enter to close)
- [ ] Responsive layout

---

### 3.3 Focus Management

**Files**: `src/ui/main_window_improved.py`, `src/ui/tab_data_driven.py`
**Complexity**: Medium
**Time Estimate**: 6 hours

**Issues:**
- No focus retention when switching tabs
- Tab order not logical in complex forms
- Enter key doesn't move to next field

**Solution:**

**In `src/ui/main_window_improved.py`:**
```python
def set_current_tab(self, section_name):
    """Set current tab by section name."""
    # Store focus widget before switch
    current_tab = self.tab_stack.currentWidget()
    if current_tab:
        self._last_focus[section_name] = current_tab.focusWidget()

    # Switch tab
    if section_name in self.tabs:
        tab = self.tabs[section_name]
        self.tab_stack.setCurrentWidget(tab)

        # Restore focus or set to first input
        if section_name in self._last_focus:
            widget = self._last_focus[section_name]
            if widget and widget.isVisible():
                widget.setFocus()
        else:
            self._focus_first_input(tab)

def _focus_first_input(self, tab):
    """Focus first input in tab."""
    # Find first focusable widget
    for widget in tab.findChildren(QWidget):
        if widget.focusPolicy() != Qt.NoFocus and widget.isEnabled():
            widget.setFocus()
            break
```

**In `src/ui/tab_data_driven.py`:**
```python
def _create_control(self, setting):
    """Create control with proper tab order."""
    widget = # ... create widget

    # Handle Enter key to move to next field
    widget.installEventFilter(self)

    return widget

def eventFilter(self, obj, event):
    """Handle Enter key for field navigation."""
    if event.type() == QEvent.KeyPress:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not event.modifiers() & Qt.ShiftModifier:
                # Move to next widget
                self.focusNextChild()
                return True
            else:
                # Shift+Enter moves to previous
                self.focusPreviousChild()
                return True
    return super().eventFilter(obj, event)
```

**Testing**:
- Switch tabs and verify focus retention
- Tab through all controls in logical order
- Press Enter to move to next field
- Press Shift+Enter to move to previous

**Acceptance Criteria:**
- [ ] Focus restored when returning to tab
- [ ] Tab order is logical (top to bottom, left to right)
- [ ] Enter moves to next field
- [ ] Shift+Enter moves to previous field
- [ ] Last field wraps to first

---

## Phase 4: Validation & Error Feedback (Week 4-5)

**Goal**: Real-time validation with clear, actionable feedback
**Priority**: High
**Complexity**: Medium

### 4.1 Enhanced Validation Framework

**File**: `src/core/validator.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Current State:**
Basic validation exists but runs only on build (batch mode).

**Solution:**
Create comprehensive real-time validation system:

```python
from dataclasses import dataclass
from typing import Optional, Callable, List
from enum import Enum

class ValidationSeverity(Enum):
    """Validation result severity."""
    ERROR = "error"      # Prevents build
    WARNING = "warning"  # Allows build with confirmation
    INFO = "info"        # Just informational

@dataclass
class ValidationResult:
    """Result of a validation check."""
    field: str
    severity: ValidationSeverity
    message: str
    suggestion: Optional[str] = None
    field_path: Optional[str] = None  # e.g., "basic.input_file"

    @property
    def is_valid(self):
        return self.severity != ValidationSeverity.ERROR

class ValidationRule:
    """Base class for validation rules."""

    def __init__(self, field, message, severity=ValidationSeverity.ERROR):
        self.field = field
        self.message = message
        self.severity = severity

    def validate(self, value, config=None) -> Optional[ValidationResult]:
        """Validate value. Return ValidationResult if invalid, None if valid."""
        raise NotImplementedError

class RequiredRule(ValidationRule):
    """Validates that field is not empty."""

    def validate(self, value, config=None):
        if not value:
            return ValidationResult(
                field=self.field,
                severity=self.severity,
                message=self.message or f"{self.field} is required",
                suggestion="Please provide a value for this field"
            )
        return None

class FileExistsRule(ValidationRule):
    """Validates that file exists."""

    def validate(self, value, config=None):
        if value and not os.path.exists(value):
            return ValidationResult(
                field=self.field,
                severity=self.severity,
                message=f"File not found: {value}",
                suggestion="Check the file path or browse to select a file"
            )
        return None

class FileExtensionRule(ValidationRule):
    """Validates file extension."""

    def __init__(self, field, extensions, **kwargs):
        super().__init__(field, **kwargs)
        self.extensions = extensions if isinstance(extensions, list) else [extensions]

    def validate(self, value, config=None):
        if value:
            ext = os.path.splitext(value)[1].lower()
            if ext not in self.extensions:
                return ValidationResult(
                    field=self.field,
                    severity=self.severity,
                    message=f"Invalid file type. Expected: {', '.join(self.extensions)}",
                    suggestion=f"Select a file with extension: {', '.join(self.extensions)}"
                )
        return None

class RealTimeValidator:
    """Real-time validation manager."""

    def __init__(self):
        self.rules = {}  # field -> [rules]
        self.last_results = {}  # field -> ValidationResult

    def add_rule(self, field_path, rule):
        """Add validation rule for field."""
        if field_path not in self.rules:
            self.rules[field_path] = []
        self.rules[field_path].append(rule)

    def validate_field(self, field_path, value, config=None) -> List[ValidationResult]:
        """Validate single field."""
        results = []

        if field_path in self.rules:
            for rule in self.rules[field_path]:
                result = rule.validate(value, config)
                if result:
                    results.append(result)

        # Cache results
        self.last_results[field_path] = results
        return results

    def validate_all(self, config) -> List[ValidationResult]:
        """Validate all fields."""
        all_results = []

        for field_path, rules in self.rules.items():
            value = config.get(field_path)
            for rule in rules:
                result = rule.validate(value, config)
                if result:
                    all_results.append(result)

        return all_results

    def get_errors(self) -> List[ValidationResult]:
        """Get all current errors."""
        errors = []
        for results in self.last_results.values():
            errors.extend([r for r in results if r.severity == ValidationSeverity.ERROR])
        return errors

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.get_errors()) > 0

# Predefined validators
def create_standard_validators():
    """Create standard validation rules."""
    validator = RealTimeValidator()

    # Input file validation
    validator.add_rule("basic.input_file",
        RequiredRule("basic.input_file", "Input file is required"))
    validator.add_rule("basic.input_file",
        FileExistsRule("basic.input_file", "Input file does not exist"))
    validator.add_rule("basic.input_file",
        FileExtensionRule("basic.input_file", [".py"],
                         message="Input must be a Python file (.py)"))

    # Output directory validation
    validator.add_rule("basic.output_dir",
        DirectoryExistsRule("basic.output_dir",
                           severity=ValidationSeverity.WARNING,
                           message="Output directory will be created if it doesn't exist"))

    # Compiler validation
    validator.add_rule("basic.compiler",
        CompilerAvailableRule("basic.compiler",
                             message="Selected compiler may not be available"))

    return validator
```

**Testing**:
- Test each validation rule independently
- Test with valid and invalid values
- Verify suggestions are helpful
- Test async validation (file checks)

**Acceptance Criteria:**
- [ ] Validation rules are composable and reusable
- [ ] Real-time validation is debounced (500ms)
- [ ] Validation results include helpful suggestions
- [ ] Async validation doesn't block UI
- [ ] Validation can be triggered manually

---

### 4.2 Inline Validation UI

**File**: `src/ui/tab_data_driven.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Solution:**
Add validation indicators to form controls:

```python
from PySide6.QtCore import QTimer

class TabDataDriven(QWidget):
    def __init__(self, ...):
        super().__init__(...)
        # ... existing init ...

        # Validation
        from ..core.validator import create_standard_validators
        self.validator = create_standard_validators()
        self.validation_timers = {}  # Debounce timers

    def _build_setting_row(self, setting):
        """Build setting row with validation."""
        row = QFrame()
        layout = QVBoxLayout(row)

        # ... existing label code ...

        # Control with validation indicator
        control_row = QHBoxLayout()
        control_widget = self._create_control(setting)
        control_row.addWidget(control_widget, 1)

        # Validation indicator
        validation_icon = QLabel()
        validation_icon.setProperty("class", "validation-icon")
        validation_icon.setFixedSize(20, 20)
        validation_icon.hide()  # Hidden until validation runs
        control_row.addWidget(validation_icon)

        layout.addLayout(control_row)

        # Validation message
        validation_msg = QLabel()
        validation_msg.setProperty("class", "validation-message")
        validation_msg.setWordWrap(True)
        validation_msg.hide()
        layout.addWidget(validation_msg)

        # Store references
        self.controls[key] = {
            "type": setting["type"],
            "widget": control_widget,
            "validation_icon": validation_icon,
            "validation_msg": validation_msg,
            "setting": setting,
        }

        # Connect validation
        self._connect_validation(key, control_widget)

        return row

    def _connect_validation(self, key, widget):
        """Connect widget changes to validation."""
        # Get field path from setting
        field_path = self.controls[key]["setting"].get("config_key", key)

        # Connect appropriate signal based on widget type
        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(
                lambda: self._schedule_validation(field_path))
        elif isinstance(widget, QComboBox):
            widget.currentTextChanged.connect(
                lambda: self._schedule_validation(field_path))
        elif isinstance(widget, QCheckBox):
            widget.stateChanged.connect(
                lambda: self._schedule_validation(field_path))
        # ... other widget types ...

    def _schedule_validation(self, field_path):
        """Schedule validation with debounce."""
        # Cancel existing timer
        if field_path in self.validation_timers:
            self.validation_timers[field_path].stop()

        # Create new timer (500ms debounce)
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._validate_field(field_path))
        timer.start(500)

        self.validation_timers[field_path] = timer

    def _validate_field(self, field_path):
        """Validate field and update UI."""
        # Get value
        value = self.config.get(field_path)

        # Run validation
        results = self.validator.validate_field(field_path, value, self.config)

        # Update UI for this field
        for key, control in self.controls.items():
            if control["setting"].get("config_key") == field_path:
                self._update_validation_ui(key, results)
                break

    def _update_validation_ui(self, key, results):
        """Update validation UI for control."""
        control = self.controls[key]
        icon = control["validation_icon"]
        msg = control["validation_msg"]

        if not results:
            # Valid - show success
            icon.setText("✓")
            icon.setProperty("validation-state", "success")
            icon.setToolTip("Valid")
            icon.setStyleSheet("color: #4A9B4A;")
            icon.show()
            msg.hide()
        else:
            # Invalid - show first error/warning
            result = results[0]

            if result.severity == ValidationSeverity.ERROR:
                icon.setText("✗")
                icon.setProperty("validation-state", "error")
                icon.setStyleSheet("color: #C93A3A;")
            elif result.severity == ValidationSeverity.WARNING:
                icon.setText("⚠")
                icon.setProperty("validation-state", "warning")
                icon.setStyleSheet("color: #E89D3F;")
            else:
                icon.setText("ℹ")
                icon.setProperty("validation-state", "info")
                icon.setStyleSheet("color: #4A7BA7;")

            icon.setToolTip(result.message)
            icon.show()

            # Show message with suggestion
            msg_text = result.message
            if result.suggestion:
                msg_text += f"\n💡 {result.suggestion}"
            msg.setText(msg_text)
            msg.show()
```

**Testing**:
- Type in fields and verify validation after 500ms
- Verify icons update correctly
- Test with valid and invalid values
- Verify tooltips show on icons
- Test suggestions are helpful

**Acceptance Criteria:**
- [ ] Validation runs 500ms after last keystroke
- [ ] Icons show validation state (✓ ✗ ⚠ ℹ)
- [ ] Error messages appear below field
- [ ] Suggestions are shown when available
- [ ] Validation doesn't impact performance

---

### 4.3 Validation Summary Panel

**File**: `src/ui/main_window_improved.py`
**Complexity**: Medium
**Time Estimate**: 6 hours

**Solution:**
Use diagnostics tab for validation summary:

```python
def _create_diagnostics_panel(self):
    """Create diagnostics panel (validation summary)."""
    panel = QWidget()
    layout = QVBoxLayout(panel)

    # Header
    header = QHBoxLayout()
    title = QLabel("Validation")
    title.setProperty("class", "panel-title")
    header.addWidget(title)

    # Clear all button
    clear_btn = QPushButton("Clear All")
    clear_btn.clicked.connect(self._clear_validations)
    header.addWidget(clear_btn)

    layout.addLayout(header)

    # Validation list
    self.validation_list = QListWidget()
    self.validation_list.setProperty("class", "validation-list")
    self.validation_list.itemClicked.connect(self._jump_to_field)
    layout.addWidget(self.validation_list)

    return panel

def update_validation_summary(self):
    """Update validation summary panel."""
    self.validation_list.clear()

    # Get all validation results
    errors = []
    warnings = []
    infos = []

    for tab in self.tabs.values():
        if hasattr(tab, 'validator'):
            for result in tab.validator.last_results.values():
                for r in result:
                    if r.severity == ValidationSeverity.ERROR:
                        errors.append(r)
                    elif r.severity == ValidationSeverity.WARNING:
                        warnings.append(r)
                    else:
                        infos.append(r)

    # Update warnings button
    total = len(errors) + len(warnings)
    self.warnings_btn.setText(f"Warnings: {total}")

    if errors:
        self.warnings_btn.setProperty("class", "danger")
    elif warnings:
        self.warnings_btn.setProperty("class", "warning")
    else:
        self.warnings_btn.setProperty("class", "")

    # Add items to list
    for error in errors:
        item = QListWidgetItem(f"✗ {error.message}")
        item.setData(Qt.UserRole, error.field_path)
        item.setForeground(QColor("#C93A3A"))
        self.validation_list.addItem(item)

    for warning in warnings:
        item = QListWidgetItem(f"⚠ {warning.message}")
        item.setData(Qt.UserRole, warning.field_path)
        item.setForeground(QColor("#E89D3F"))
        self.validation_list.addItem(item)

    for info in infos:
        item = QListWidgetItem(f"ℹ {info.message}")
        item.setData(Qt.UserRole, info.field_path)
        item.setForeground(QColor("#4A7BA7"))
        self.validation_list.addItem(item)

def _jump_to_field(self, item):
    """Jump to field when validation item clicked."""
    field_path = item.data(Qt.UserRole)

    # Parse field path (e.g., "basic.input_file")
    parts = field_path.split(".")
    if len(parts) >= 1:
        section = parts[0]

        # Switch to tab
        self.set_current_tab(section)

        # Focus field in tab
        if section in self.tabs:
            tab = self.tabs[section]
            if hasattr(tab, 'focus_field'):
                tab.focus_field(field_path)
```

**Testing**:
- Trigger validation errors in multiple fields
- Verify summary shows all issues
- Click items and verify focus jumps to field
- Verify counter updates
- Test clear all button

**Acceptance Criteria:**
- [ ] Summary shows all validation issues
- [ ] Issues grouped by severity (errors first)
- [ ] Click item jumps to problematic field
- [ ] Counter shows total issues
- [ ] Updates in real-time as validation runs

---

## Phase 5: Visual Hierarchy & Information Density (Week 5-6)

**Goal**: Optimize information architecture and visual design
**Priority**: Medium
**Complexity**: Medium

### 5.1 Typography Scale Enhancement

**File**: `src/ui/styles.py`
**Complexity**: Simple
**Time Estimate**: 3 hours

**Current Issues:**
- Weak hierarchy (only 3pt difference between levels)
- No consistent scale
- Font weights not used effectively

**Solution:**
Implement proper type scale:

```python
# Typography scale (based on 1.25 ratio)
TYPOGRAPHY = {
    "xs": {
        "size": "9pt",
        "weight": 400,
        "line_height": 1.4,
        "letter_spacing": "0",
    },
    "sm": {
        "size": "10pt",
        "weight": 400,
        "line_height": 1.5,
        "letter_spacing": "0",
    },
    "base": {
        "size": "11pt",  # Body text
        "weight": 400,
        "line_height": 1.5,
        "letter_spacing": "0",
    },
    "md": {
        "size": "13pt",  # Section labels
        "weight": 600,
        "line_height": 1.4,
        "letter_spacing": "0.01em",
    },
    "lg": {
        "size": "16pt",  # Headers
        "weight": 600,
        "line_height": 1.3,
        "letter_spacing": "0.01em",
    },
    "xl": {
        "size": "20pt",  # Page titles
        "weight": 700,
        "line_height": 1.2,
        "letter_spacing": "0.02em",
    },
    "2xl": {
        "size": "24pt",  # App name
        "weight": 700,
        "line_height": 1.1,
        "letter_spacing": "0.02em",
    },
}

# Apply in QSS
def build_qss(colors, spacing, typography):
    return f'''
    /* Typography classes */
    .text-xs {{ font-size: {typography["xs"]["size"]}; font-weight: {typography["xs"]["weight"]}; }}
    .text-sm {{ font-size: {typography["sm"]["size"]}; font-weight: {typography["sm"]["weight"]}; }}
    .text-base {{ font-size: {typography["base"]["size"]}; font-weight: {typography["base"]["weight"]}; }}
    .text-md {{ font-size: {typography["md"]["size"]}; font-weight: {typography["md"]["weight"]}; }}
    .text-lg {{ font-size: {typography["lg"]["size"]}; font-weight: {typography["lg"]["weight"]}; }}
    .text-xl {{ font-size: {typography["xl"]["size"]}; font-weight: {typography["xl"]["weight"]}; }}
    .text-2xl {{ font-size: {typography["2xl"]["size"]}; font-weight: {typography["2xl"]["weight"]}; }}

    /* Section title */
    .section-title {{
        font-size: {typography["lg"]["size"]};
        font-weight: {typography["lg"]["weight"]};
        letter-spacing: {typography["lg"]["letter_spacing"]};
        margin-bottom: {spacing["md"]};
    }}

    /* Panel title */
    .panel-title {{
        font-size: {typography["md"]["size"]};
        font-weight: {typography["md"]["weight"]};
        letter-spacing: {typography["md"]["letter_spacing"]};
    }}
    '''
```

**Testing**:
- Visual review of all text sizes
- Verify hierarchy is clear
- Test at different zoom levels
- Compare before/after screenshots

**Acceptance Criteria:**
- [ ] Clear visual hierarchy (5+ distinct levels)
- [ ] Consistent scale based on ratio
- [ ] Font weights used appropriately
- [ ] Line heights comfortable for reading

---

### 5.2 Spacing System Enhancement

**File**: `src/ui/styles.py`
**Complexity**: Simple
**Time Estimate**: 3 hours

**Solution:**
Expand spacing system:

```python
# Spacing scale (4px base)
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
    "4xl": "64px",
}

# Apply consistently in QSS
'''
/* Margin utilities */
.m-xs {{ margin: {spacing["xs"]}; }}
.m-sm {{ margin: {spacing["sm"]}; }}
.m-md {{ margin: {spacing["md"]}; }}
.m-lg {{ margin: {spacing["lg"]}; }}
.m-xl {{ margin: {spacing["xl"]}; }}

/* Padding utilities */
.p-xs {{ padding: {spacing["xs"]}; }}
.p-sm {{ padding: {spacing["sm"]}; }}
.p-md {{ padding: {spacing["md"]}; }}
.p-lg {{ padding: {spacing["lg"]}; }}
.p-xl {{ padding: {spacing["xl"]}; }}

/* Section spacing */
QGroupBox {{
    margin-top: {spacing["lg"]};
    padding: {spacing["lg"]};
}}

/* Card spacing */
.card {{
    padding: {spacing["xl"]};
    margin: {spacing["md"]};
}}
'''
```

**Testing**:
- Visual review of spacing
- Verify consistency across tabs
- Check spacing at different window sizes

**Acceptance Criteria:**
- [ ] Consistent spacing throughout app
- [ ] 4px base unit used everywhere
- [ ] Adequate whitespace between elements
- [ ] No arbitrary spacing values

---

### 5.3 Progressive Disclosure

**File**: `src/ui/tab_data_driven.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Solution:**
Group settings by risk and make collapsible:

```python
def _build_ui(self):
    """Build UI with progressive disclosure."""
    # Group settings by risk
    safe_settings = []
    caution_settings = []
    risky_settings = []
    expert_settings = []

    for setting in self.settings:
        risk = setting.get("risk", "safe")
        if risk == "safe":
            safe_settings.append(setting)
        elif risk == "caution":
            caution_settings.append(setting)
        elif risk == "risky":
            risky_settings.append(setting)
        elif risk == "expert":
            expert_settings.append(setting)

    # Always show safe settings
    if safe_settings:
        safe_section = self._create_section("Basic Settings", safe_settings, collapsible=False)
        self.layout.addWidget(safe_section)

    # Caution - collapsible, expanded by default
    if caution_settings:
        caution_section = self._create_section(
            "⚠ Advanced Settings",
            caution_settings,
            collapsible=True,
            expanded=True
        )
        self.layout.addWidget(caution_section)

    # Risky - collapsible, collapsed by default
    if risky_settings:
        risky_section = self._create_section(
            "🔥 Expert Settings",
            risky_settings,
            collapsible=True,
            expanded=False
        )
        self.layout.addWidget(risky_section)

    # Expert - collapsible, collapsed by default
    if expert_settings:
        expert_section = self._create_section(
            "⚡ Experimental",
            expert_settings,
            collapsible=True,
            expanded=False
        )
        self.layout.addWidget(expert_section)

def _create_section(self, title, settings, collapsible=False, expanded=True):
    """Create section with optional collapsibility."""
    from .widgets import CollapsibleFrame

    if collapsible:
        section = CollapsibleFrame(title, expanded=expanded)
        content = QWidget()
        layout = QVBoxLayout(content)

        for setting in settings:
            row = self._build_setting_row(setting)
            layout.addWidget(row)

        section.set_content(content)
    else:
        section = QGroupBox(title)
        layout = QVBoxLayout(section)

        for setting in settings:
            row = self._build_setting_row(setting)
            layout.addWidget(row)

    return section
```

**Testing**:
- Verify settings grouped correctly by risk
- Test expand/collapse animations
- Verify state persists in config
- Test with keyboard (Space to expand/collapse)

**Acceptance Criteria:**
- [ ] Settings grouped by risk level
- [ ] Safe settings always visible
- [ ] Advanced/expert settings collapsed by default
- [ ] Expansion state saved to config
- [ ] Smooth expand/collapse animation

---

## Phase 6: Modern UI Patterns (Week 6-7)

**Goal**: Replace modal dialogs, add modern interactions
**Priority**: Medium
**Complexity**: Medium-Complex

### 6.1 Toast Notification System

**File**: New file `src/ui/toast.py`
**Complexity**: Medium
**Time Estimate**: 8 hours

**Solution:**
Create non-blocking toast notifications:

```python
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QColor

class Toast(QWidget):
    """A single toast notification."""

    def __init__(self, message, type="info", duration=3000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.type = type  # "success", "error", "warning", "info"
        self.duration = duration

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Icon
        icon = self._get_icon(type)
        icon_label = QLabel(icon)
        icon_label.setProperty("class", "toast-icon")
        layout.addWidget(icon_label)

        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setProperty("class", "toast-message")
        layout.addWidget(message_label, 1)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setProperty("class", "toast-close")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.dismiss)
        layout.addWidget(close_btn)

        # Style based on type
        self.setProperty("toast-type", type)

        # Auto-dismiss timer
        if duration > 0:
            QTimer.singleShot(duration, self.dismiss)

    def _get_icon(self, type):
        """Get icon for toast type."""
        icons = {
            "success": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "ℹ",
        }
        return icons.get(type, "ℹ")

    def dismiss(self):
        """Dismiss toast with animation."""
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(200)
        anim.setEndValue(QPoint(self.x() + self.width(), self.y()))
        anim.setEasingCurve(QEasingCurve.InOutCubic)
        anim.finished.connect(self.close)
        anim.start()

    def paintEvent(self, event):
        """Paint toast background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background color based on type
        colors = {
            "success": QColor(74, 155, 74, 240),
            "error": QColor(201, 58, 58, 240),
            "warning": QColor(232, 157, 63, 240),
            "info": QColor(74, 123, 167, 240),
        }
        color = colors.get(self.type, colors["info"])

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 8, 8)


class ToastManager(QWidget):
    """Manages multiple toast notifications."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(16, 16, 16, 16)

        self.toasts = []

    def show_toast(self, message, type="info", duration=3000):
        """Show a toast notification."""
        toast = Toast(message, type, duration)

        # Add to layout
        self.layout.addWidget(toast)
        self.toasts.append(toast)

        # Position manager
        parent_rect = self.parent().rect() if self.parent() else self.screen().geometry()
        self.setGeometry(
            parent_rect.right() - 400,
            16,
            380,
            parent_rect.height() - 32
        )
        self.show()

        # Slide in animation
        toast.move(self.width(), toast.y())
        anim = QPropertyAnimation(toast, b"pos")
        anim.setDuration(300)
        anim.setStartValue(QPoint(self.width(), toast.y()))
        anim.setEndValue(QPoint(0, toast.y()))
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        # Clean up when toast closes
        toast.destroyed.connect(lambda: self._remove_toast(toast))

        return toast

    def _remove_toast(self, toast):
        """Remove toast from list."""
        if toast in self.toasts:
            self.toasts.remove(toast)

        # Hide manager if no toasts
        if not self.toasts:
            self.hide()
```

**Integration in `src/ui/main_window_improved.py`:**
```python
from .toast import ToastManager

class MainWindow(QMainWindow):
    def __init__(self, ...):
        # ... existing init ...

        # Toast manager
        self.toast_manager = ToastManager(self)

    def show_toast(self, message, type="info", duration=3000):
        """Show toast notification."""
        return self.toast_manager.show_toast(message, type, duration)
```

**Replace modal dialogs in `src/app.py`:**
```python
# Before:
QMessageBox.information(self, "Success", "Configuration saved!")

# After:
self.main_window.show_toast("Configuration saved!", "success")
```

**Testing**:
- Show multiple toasts simultaneously
- Test all toast types (success, error, warning, info)
- Verify auto-dismiss works
- Test manual dismiss
- Verify animations are smooth
- Test on different screen sizes

**Acceptance Criteria:**
- [ ] Toasts slide in from top-right
- [ ] Multiple toasts stack vertically
- [ ] Auto-dismiss after duration
- [ ] Manual dismiss with X button
- [ ] Smooth animations (300ms)
- [ ] Toasts don't block interaction

---

### 6.2 Drag & Drop Support

**File**: `src/ui/widgets.py`
**Complexity**: Medium
**Time Estimate**: 6 hours

**Solution:**
Add drag & drop to file inputs:

```python
class FileSelectFrame(QFrame):
    """File/directory picker with drag & drop support."""

    def __init__(self, ...):
        # ... existing init ...

        # Enable drag & drop
        self.setAcceptDrops(True)
        self.entry.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # Visual feedback
            self.setProperty("drag-active", True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        """Handle drag leave."""
        self.setProperty("drag-active", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event):
        """Handle drop."""
        self.setProperty("drag-active", False)
        self.style().unpolish(self)
        self.style().polish(self)

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()

                # Validate dropped file
                if self.mode == "file":
                    if os.path.isfile(path):
                        self.set_path(path)
                        event.acceptProposedAction()
                    else:
                        # Show error toast
                        from .toast import show_toast
                        show_toast("Dropped item is not a file", "error")
                elif self.mode == "directory":
                    if os.path.isdir(path):
                        self.set_path(path)
                        event.acceptProposedAction()
                    else:
                        show_toast("Dropped item is not a directory", "error")
```

**Add drop styling in `src/ui/styles.py`:**
```css
/* Drag & drop states */
FileSelectFrame[drag-active="true"] {
    border: 2px dashed #D07A2D;
    background-color: rgba(208, 122, 45, 0.1);
}

QLineEdit[drag-active="true"] {
    border: 2px dashed #D07A2D;
    background-color: rgba(208, 122, 45, 0.1);
}
```

**Testing**:
- Drag file onto input field
- Drag directory onto directory picker
- Drag invalid type and verify error
- Test drop indicator styling
- Test on all platforms

**Acceptance Criteria:**
- [ ] Files can be dragged onto file inputs
- [ ] Directories can be dragged onto directory inputs
- [ ] Visual feedback during drag
- [ ] Invalid drops show error message
- [ ] Works on Windows, macOS, Linux

---

## Phase 7: Polish & Performance (Week 7-8)

**Goal**: Final refinements and optimization
**Priority**: Low-Medium
**Complexity**: Simple-Medium

### 7.1 Loading States

**Files**: Various
**Complexity**: Medium
**Time Estimate**: 6 hours

**Solution:**
Add loading indicators:

```python
# In src/ui/widgets.py
class LoadingSpinner(QWidget):
    """Animated loading spinner."""

    def __init__(self, size=24, parent=None):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.setFixedSize(size, size)

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._rotate)

    def start(self):
        """Start spinning."""
        self.timer.start(50)  # 20 FPS
        self.show()

    def stop(self):
        """Stop spinning."""
        self.timer.stop()
        self.hide()

    def _rotate(self):
        """Rotate spinner."""
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        """Paint spinner."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw spinning arc
        painter.translate(self.size / 2, self.size / 2)
        painter.rotate(self.angle)

        pen = QPen(QColor("#D07A2D"), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(-self.size/2 + 3, -self.size/2 + 3,
                       self.size - 6, self.size - 6,
                       0, 270 * 16)  # 270 degree arc

# Use in file operations
class FileSelectFrame(QFrame):
    def browse(self):
        """Browse for file with loading state."""
        # Show spinner during file dialog
        spinner = LoadingSpinner(parent=self)
        spinner.move(self.width() - 30, (self.height() - 24) / 2)
        spinner.start()

        # File dialog
        if self.mode == "file":
            path, _ = QFileDialog.getOpenFileName(...)
        else:
            path = QFileDialog.getExistingDirectory(...)

        spinner.stop()

        if path:
            self.set_path(path)
```

**Testing**:
- Test spinner animation smoothness
- Verify spinner appears during slow operations
- Test on slow file systems
- Verify spinner stops correctly

**Acceptance Criteria:**
- [ ] Spinner appears for operations > 200ms
- [ ] Animation is smooth (20+ FPS)
- [ ] Spinner positioned correctly
- [ ] Spinner stops when operation completes

---

### 7.2 Empty States

**File**: `src/ui/main_window_improved.py`
**Complexity**: Simple
**Time Estimate**: 3 hours

**Solution:**
Add helpful empty states:

```python
def _create_artifacts_panel(self):
    """Create artifacts panel with empty state."""
    panel = QWidget()
    layout = QVBoxLayout(panel)

    # ... existing header ...

    # Stacked widget (empty state / artifact list)
    self.artifacts_stack = QStackedWidget()

    # Empty state
    empty_widget = QWidget()
    empty_layout = QVBoxLayout(empty_widget)
    empty_layout.setAlignment(Qt.AlignCenter)

    empty_icon = QLabel("📦")
    empty_icon.setProperty("class", "empty-icon")
    empty_icon.setAlignment(Qt.AlignCenter)
    empty_layout.addWidget(empty_icon)

    empty_text = QLabel("No artifacts yet")
    empty_text.setProperty("class", "empty-text")
    empty_text.setAlignment(Qt.AlignCenter)
    empty_layout.addWidget(empty_text)

    empty_hint = QLabel("Run a build to see compiled outputs here")
    empty_hint.setProperty("class", "empty-hint")
    empty_hint.setAlignment(Qt.AlignCenter)
    empty_layout.addWidget(empty_hint)

    build_btn = QPushButton("Build Now")
    build_btn.setProperty("class", "primary")
    build_btn.clicked.connect(self.compile_code)
    empty_layout.addWidget(build_btn, alignment=Qt.AlignCenter)

    self.artifacts_stack.addWidget(empty_widget)

    # Artifact list
    self.artifacts_table = QTableWidget()
    # ... existing table setup ...
    self.artifacts_stack.addWidget(self.artifacts_table)

    layout.addWidget(self.artifacts_stack)

    return panel

def populate_artifacts(self):
    """Populate artifacts (show empty state if none)."""
    # ... existing population code ...

    if self.artifacts_table.rowCount() == 0:
        self.artifacts_stack.setCurrentIndex(0)  # Show empty state
    else:
        self.artifacts_stack.setCurrentIndex(1)  # Show table
```

**Add empty state styling in `src/ui/styles.py`:**
```css
/* Empty states */
.empty-icon {
    font-size: 64pt;
    margin-bottom: 16px;
    opacity: 0.5;
}

.empty-text {
    font-size: 18pt;
    font-weight: 600;
    margin-bottom: 8px;
}

.empty-hint {
    font-size: 11pt;
    color: #8B8578;
    margin-bottom: 24px;
}
```

**Testing**:
- Verify empty state appears when no data
- Test action button works
- Verify transition to populated state
- Test on all tabs with empty states

**Acceptance Criteria:**
- [ ] Empty states appear when appropriate
- [ ] Helpful hints and actions provided
- [ ] Smooth transition to populated state
- [ ] Consistent styling across all empty states

---

## Phase 8: Documentation & Testing (Week 8)

**Goal**: Comprehensive testing and documentation
**Priority**: Critical
**Complexity**: Medium

### 8.1 Accessibility Testing

**Testing Protocol:**

**Screen Reader Testing:**
- [ ] **NVDA (Windows)**: Test all tabs, forms, dialogs
- [ ] **JAWS (Windows)**: Verify compatibility
- [ ] **VoiceOver (macOS)**: Test navigation
- [ ] **Orca (Linux)**: Basic functionality test

**Keyboard Testing:**
- [ ] Tab through entire application
- [ ] Test all keyboard shortcuts
- [ ] Verify focus indicators visible
- [ ] Test form navigation (Tab, Shift+Tab, Enter)
- [ ] Test without mouse for 30 minutes

**Contrast Testing:**
- [ ] Run WebAIM Contrast Checker on all text
- [ ] Test in high contrast mode (Windows)
- [ ] Test with color blindness simulators
- [ ] Verify icons work without color

**Testing Tools:**
- WAVE browser extension
- axe DevTools
- Color Oracle (color blindness simulator)
- Contrast checker browser extension

**Acceptance Criteria:**
- [ ] WCAG 2.1 AA compliance verified
- [ ] All interactive elements keyboard accessible
- [ ] Screen reader announces all content correctly
- [ ] Color is not sole means of conveying information

---

### 8.2 Cross-Platform Testing

**Testing Protocol:**

**Windows 10/11:**
- [ ] Test on different DPI settings (100%, 125%, 150%, 200%)
- [ ] Test with Windows dark mode
- [ ] Test with high contrast themes
- [ ] Verify native look and feel

**macOS (Monterey+):**
- [ ] Test on Retina displays
- [ ] Test with macOS dark mode
- [ ] Test with Reduce Motion enabled
- [ ] Verify native look and feel

**Linux (Ubuntu 22.04+):**
- [ ] Test on different desktop environments (GNOME, KDE)
- [ ] Test with system dark themes
- [ ] Test on high-DPI displays
- [ ] Verify Qt theme integration

**Issues to Watch For:**
- Font rendering differences
- Color rendering on different displays
- Layout issues at different DPI
- Keyboard shortcut conflicts
- File dialog behavior
- Theme integration

**Acceptance Criteria:**
- [ ] Application works on all three platforms
- [ ] No platform-specific crashes
- [ ] UI looks native on each platform
- [ ] All features work correctly

---

### 8.3 Performance Testing

**Testing Protocol:**

**Startup Performance:**
- [ ] Measure application startup time
- [ ] Profile JSON loading
- [ ] Profile stylesheet generation
- [ ] Target: < 2 seconds on modern hardware

**Runtime Performance:**
- [ ] Test theme switching speed (target: < 500ms)
- [ ] Test tab switching speed (target: < 100ms)
- [ ] Test validation responsiveness (target: < 200ms after debounce)
- [ ] Profile memory usage over time

**Optimization Techniques:**
- Lazy load tabs (only create on first view)
- Cache compiled stylesheets
- Debounce validation (500ms)
- Use QWidget.setUpdatesEnabled() during bulk updates

**Profiling Tools:**
- Python cProfile
- Qt Performance Analyzer
- Memory Profiler
- CPU profiler

**Acceptance Criteria:**
- [ ] Startup < 2 seconds
- [ ] Theme switch < 500ms
- [ ] Tab switch < 100ms
- [ ] No memory leaks over 1 hour session
- [ ] CPU usage < 5% when idle

---

### 8.4 Documentation Updates

**Documentation Tasks:**

**README.md Updates:**
```markdown
## Features

### Accessibility
- WCAG 2.1 AA compliant
- Full keyboard navigation
- Screen reader compatible
- High contrast mode support

### User Experience
- Light and dark themes
- Real-time validation
- Non-blocking notifications
- Drag & drop support
- Keyboard shortcuts for all actions

### Modern UI
- Industrial warm design
- Progressive disclosure
- Inline error feedback
- Command palette (Ctrl+P)
- Toast notifications
```

**Keyboard Shortcuts Documentation:**
Create `KEYBOARD_SHORTCUTS.md`:
```markdown
# Keyboard Shortcuts

## File Operations
- `Ctrl+N` - New Configuration
- `Ctrl+O` - Open Configuration
- `Ctrl+S` - Save Configuration
- `Ctrl+Shift+S` - Save As

## Build Operations
- `F5` - Start Build
- `Shift+F5` - Stop Build
- `Ctrl+Shift+V` - Validate Configuration
- `Ctrl+K` - Show Nuitka Command

## View
- `Ctrl+F` - Find Setting
- `Ctrl+T` - Toggle Theme
- `Ctrl+`` - Toggle Console
- `Ctrl+?` - Show Shortcuts

## Navigation
- `Ctrl+Tab` - Next Tab
- `Ctrl+Shift+Tab` - Previous Tab
- `Alt+1` ... `Alt+6` - Jump to Tab
```

**Accessibility Documentation:**
Create `ACCESSIBILITY.md`:
```markdown
# Accessibility Features

## Screen Reader Support
- All interactive elements have accessible labels
- Form labels properly associated
- State changes announced
- Live regions for dynamic content

## Keyboard Navigation
- Full keyboard access to all features
- Visible focus indicators
- Logical tab order
- Skip links for main content

## Visual Accessibility
- WCAG 2.1 AA compliant color contrast
- 11pt minimum font size
- Resizable text (up to 200%)
- High contrast mode compatible

## Reduced Motion
- Respects system reduced motion preference
- All animations can be disabled
```

**Developer Guide:**
Create `DEVELOPER_GUIDE.md` with:
- Architecture overview
- Adding new settings
- Extending validation
- Theme customization
- Widget development guide

---

## Implementation Priority Matrix

### Must Have (Critical Path) - Weeks 1-5

| Phase | Priority | User Impact | Complexity | Dependencies |
|-------|----------|-------------|------------|--------------|
| **Phase 1: Accessibility** | 🔴 Critical | High | Medium | None |
| **Phase 2: Dark Mode** | 🟠 High | High | Medium | Phase 1 |
| **Phase 3: Keyboard Nav** | 🟠 High | High | Medium | Phase 1 |
| **Phase 4: Validation** | 🟠 High | Very High | Medium | None |

**Rationale**: These phases address critical accessibility violations, implement highly requested features (dark mode), and significantly improve usability through validation and keyboard support.

### Should Have (Enhancement) - Weeks 5-7

| Phase | Priority | User Impact | Complexity | Dependencies |
|-------|----------|-------------|------------|--------------|
| **Phase 5: Visual Hierarchy** | 🟡 Medium | Medium | Medium | Phases 1-2 |
| **Phase 6: Modern UI** | 🟡 Medium | Medium | Complex | Phases 1-4 |

**Rationale**: These phases modernize the UI and improve information architecture, enhancing the overall user experience but not critical for basic functionality.

### Nice to Have (Polish) - Weeks 7-8

| Phase | Priority | User Impact | Complexity | Dependencies |
|-------|----------|-------------|------------|--------------|
| **Phase 7: Polish** | 🟢 Low | Low | Simple | All previous |
| **Phase 8: Testing & Docs** | 🔴 Critical | N/A | Medium | All previous |

**Rationale**: Phase 7 adds final polish that improves feel but not function. Phase 8 is critical for quality assurance but happens last.

---

## Success Metrics

### Accessibility Metrics
- ✓ **WCAG Compliance**: 100% AA compliance (automated audit with axe)
- ✓ **Keyboard Navigation**: All features accessible without mouse
- ✓ **Screen Reader**: Compatible with NVDA, JAWS, VoiceOver
- ✓ **Contrast Ratios**: All text meets 4.5:1 minimum

### Usability Metrics
- ✓ **Task Completion Time**: 30% reduction in average time
- ✓ **Error Rate**: 50% reduction in validation errors
- ✓ **User Satisfaction**: 80%+ satisfaction in user testing
- ✓ **Feature Discovery**: 80%+ can find settings without search

### Performance Metrics
- ✓ **Startup Time**: < 2 seconds on modern hardware
- ✓ **Theme Switch**: < 500ms with smooth transition
- ✓ **Tab Switch**: < 100ms perceived lag
- ✓ **Validation**: < 200ms response after 500ms debounce

### Adoption Metrics
- ✓ **Dark Mode**: 40%+ of users switch to dark theme
- ✓ **Keyboard Shortcuts**: 30%+ use keyboard shortcuts regularly
- ✓ **Validation**: 90%+ see validation before building

---

## Risk Assessment & Mitigation

### High Risk

**1. Dark Mode System Integration**
- **Risk**: Qt 6.5+ required for automatic theme detection
- **Impact**: Users on older Qt may not get auto-theme
- **Mitigation**: Manual toggle works on all versions; graceful fallback

**2. Screen Reader Compatibility**
- **Risk**: Custom widgets may not work with all screen readers
- **Impact**: Some users unable to use application
- **Mitigation**: Extensive testing; fall back to native widgets if needed

**3. Performance Impact of Real-Time Validation**
- **Risk**: Validation on every keystroke could slow UI
- **Impact**: Sluggish user experience
- **Mitigation**: Debouncing (500ms), async validation, caching

### Medium Risk

**4. Cross-Platform Consistency**
- **Risk**: Qt renders differently on each platform
- **Impact**: Inconsistent look/feel across platforms
- **Mitigation**: Platform-specific testing, conditional styling

**5. Theme Color Accuracy**
- **Risk**: Colors may look different on various displays
- **Impact**: Contrast ratios may fail on some screens
- **Mitigation**: Test on multiple display types, provide high contrast mode

**6. Backward Compatibility**
- **Risk**: Config format changes could break old configs
- **Impact**: Users lose saved configurations
- **Mitigation**: Config migration system already exists (tested)

### Low Risk

**7. Animation Performance**
- **Risk**: Animations may be janky on slower hardware
- **Impact**: Perceived poor quality
- **Mitigation**: Respect system reduced motion, use hardware acceleration

**8. Keyboard Shortcut Conflicts**
- **Risk**: Shortcuts may conflict with system or IDE
- **Impact**: Some shortcuts don't work
- **Mitigation**: Make shortcuts configurable, follow platform conventions

---

## Testing Strategy

### Unit Testing
```python
# Test validation rules
def test_required_rule():
    rule = RequiredRule("test_field")
    assert rule.validate("") is not None
    assert rule.validate("value") is None

# Test theme manager
def test_theme_switching():
    manager = ThemeManager()
    assert manager.current_theme == "light"
    manager.switch_theme(app, "dark")
    assert manager.current_theme == "dark"
```

### Integration Testing
- Config load/save with new fields
- Theme persistence across restarts
- Validation across multiple tabs
- Keyboard navigation flow

### Manual QA Checklist
- [ ] All accessibility requirements met
- [ ] All keyboard shortcuts work
- [ ] Theme switching works correctly
- [ ] Validation provides helpful feedback
- [ ] No regressions in existing features
- [ ] Cross-platform testing complete

---

## Dependencies & Constraints

### Technical Dependencies
- **PySide6**: 6.x (already in use)
  - Theme detection requires 6.5+ (optional feature)
- **Python**: 3.8+ (already required)
- **Operating Systems**: Windows 10+, macOS 12+, Linux (modern distros)

### External Constraints
- ✅ Must maintain backward compatibility with existing config files
- ✅ Must preserve industrial warm theme aesthetic
- ✅ Must work on all supported platforms
- ✅ Cannot break existing command generation
- ✅ Must not require additional dependencies

### Internal Constraints
- Work in 8-week sprints
- Test on all platforms before each release
- Maintain code quality (linting, type hints)
- Document all public APIs

---

## Next Steps

### Immediate Actions (This Week)
1. **Review & Approve Plan** - Stakeholder sign-off
2. **Set Up Testing Infrastructure** - Install screen readers, contrast tools
3. **Create Feature Branch** - `feature/ui-ux-improvements`
4. **Begin Phase 1** - Start with color contrast fixes

### Weekly Milestones
- **Week 1**: Phases 1.1-1.2 complete (contrast, fonts)
- **Week 2**: Phases 1.3-2.1 complete (ARIA, dark colors)
- **Week 3**: Phases 2.2-3.1 complete (theme system, shortcuts)
- **Week 4**: Phases 3.2-4.1 complete (focus, validation framework)
- **Week 5**: Phases 4.2-5.1 complete (validation UI, typography)
- **Week 6**: Phases 5.2-6.1 complete (spacing, toasts)
- **Week 7**: Phases 6.2-7.2 complete (drag-drop, polish)
- **Week 8**: Phase 8 complete (testing, documentation)

### Success Celebration
- Before/after comparison video
- Blog post about accessibility improvements
- User feedback collection
- Performance metrics comparison

---

**Document Version**: 1.0
**Last Updated**: 2026-01-15
**Status**: Ready for Implementation
**Estimated Effort**: 8 weeks (1 developer)
**Review Date**: Weekly progress reviews, final review at week 8

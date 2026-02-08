# Bug Fix Plan for Nuitka GUI Tool

This document outlines all identified bugs and the plan to fix them, organized by priority.

## Table of Contents
- [Critical Issues](#critical-issues)
- [High Priority Issues](#high-priority-issues)
- [Medium Priority Issues](#medium-priority-issues)
- [Low Priority Issues](#low-priority-issues)
- [Implementation Strategy](#implementation-strategy)

---

## Critical Issues

### 1. Missing Error Handling in `populate_artifacts()`
**File:** `src/ui/main_window_improved.py` (lines 666-678)
**Status:** 🔴 Critical
**Impact:** Application crash if file becomes inaccessible during listing

#### Problem
```python
files = [p for p in base_path.rglob("*") if p.is_file()]
for path in files:
    row = self.artifacts_table.rowCount()
    self.artifacts_table.insertRow(row)
    rel = str(path.relative_to(base_path))
    size = path.stat().st_size  # <- Can raise OSError
    mtime = path.stat().st_mtime  # <- Can raise OSError
```

#### Solution
Wrap file operations in try-except blocks:
```python
files = [p for p in base_path.rglob("*") if p.is_file()]
for path in files:
    try:
        row = self.artifacts_table.rowCount()
        self.artifacts_table.insertRow(row)
        rel = str(path.relative_to(base_path))
        stat_info = path.stat()
        size = stat_info.st_size
        mtime = stat_info.st_mtime
        # ... rest of code
    except (OSError, PermissionError) as e:
        # Log error and skip this file
        continue
```

---

## High Priority Issues

### 2. Missing Error Handling in Setting Definitions Loader
**File:** `src/core/setting_definitions.py` (lines 86-87)
**Status:** 🟠 High
**Impact:** Application won't start if settings file is missing or corrupted

#### Problem
```python
def load_setting_definitions(path: Optional[Path] = None) -> SettingRegistry:
    target = path or get_definitions_path()
    with target.open("r", encoding="utf-8") as handle:  # <- Can raise FileNotFoundError
        data = json.load(handle)  # <- Can raise JSONDecodeError
    registry = SettingRegistry(data)
```

#### Solution
Add proper error handling with fallback:
```python
def load_setting_definitions(path: Optional[Path] = None) -> SettingRegistry:
    target = path or get_definitions_path()
    try:
        with target.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return SettingRegistry(data)
    except FileNotFoundError:
        raise RuntimeError(f"Settings definition file not found: {target}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in settings file: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to load settings: {e}")
```

### 3. Improper Import Placement in `tab_data.py`
**File:** `src/ui/tab_data.py` (lines 126, 146)
**Status:** 🟠 High
**Impact:** Performance degradation, poor code quality

#### Problem
```python
def _add_data_file(self):
    source, _ = QFileDialog.getOpenFileName(self, "Select data file")
    if not source:
        return None
    import os  # <- Should be at module level
```

#### Solution
Move import to top of file:
```python
# At top of tab_data.py
import os
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QInputDialog
# ... rest of imports
```

### 4. Generic Exception Handling in Platform Detector
**File:** `src/core/platform_detector.py` (lines 82-83, 103-104)
**Status:** 🟠 High
**Impact:** Masks real errors, makes debugging difficult

#### Problem
```python
@staticmethod
def has_nuitka():
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'nuitka', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:  # <- Too broad
        return False
```

#### Solution
Use specific exception types:
```python
@staticmethod
def has_nuitka():
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'nuitka', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return False
    except subprocess.SubprocessError as e:
        # Log unexpected subprocess errors
        print(f"Unexpected error checking for Nuitka: {e}")
        return False
```

---

## Medium Priority Issues

### 5. Console Print Statements Instead of UI Feedback
**Files:** `src/core/config.py` (lines 190, 220), `src/core/executor.py` (line 73)
**Status:** 🟡 Medium
**Impact:** Users don't see error messages in the GUI

#### Problem
```python
# config.py
except Exception as e:
    print(f"Error saving configuration: {e}")  # <- Not visible in GUI
    return False
```

#### Solution
Replace with proper error handling mechanism:
```python
# Option 1: Return error message
def save_config(self, filepath: str) -> tuple[bool, str]:
    try:
        # ... save logic
        return True, "Configuration saved successfully"
    except IOError as e:
        return False, f"Failed to save configuration: {e}"
    except json.JSONDecodeError as e:
        return False, f"Invalid configuration data: {e}"

# Option 2: Use Qt signals/slots
class ConfigManager(QObject):
    error_occurred = Signal(str)

    def save_config(self, filepath: str) -> bool:
        try:
            # ... save logic
            return True
        except Exception as e:
            self.error_occurred.emit(f"Error saving configuration: {e}")
            return False
```

### 6. Broad Exception Handling in Config Manager
**File:** `src/core/config.py` (lines 189-191, 219-221)
**Status:** 🟡 Medium
**Impact:** Hides specific error causes

#### Solution
Replace generic exceptions with specific ones:
```python
def save_config(self, filepath: str) -> bool:
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=2)
        return True
    except (IOError, PermissionError) as e:
        self.error_occurred.emit(f"Cannot write to file: {e}")
        return False
    except TypeError as e:
        self.error_occurred.emit(f"Invalid configuration data: {e}")
        return False
```

### 7. Generic Exception in Compilation Executor
**File:** `src/core/executor.py` (lines 72-73, 144)
**Status:** 🟡 Medium
**Impact:** Masks specific process errors

#### Solution
```python
def stop(self):
    try:
        if self.process and self.process.poll() is None:
            self.stop_flag = True
            self.process.terminate()
            self.process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        self.process.kill()
        self.error_callback("Process forcibly terminated")
    except (ProcessLookupError, PermissionError) as e:
        self.error_callback(f"Failed to stop process: {e}")
```

---

## Low Priority Issues

### 8. Subprocess Output Handling Race Condition
**File:** `src/core/executor.py` (lines 114-130)
**Status:** 🟢 Low
**Impact:** Rare crash if process terminates unexpectedly

#### Solution
Add defensive checks:
```python
self.process = subprocess.Popen(
    self.command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True
)

if self.process.stdout:
    for line in self.process.stdout:
        if self.stop_flag:
            break
        if self.output_callback:
            self.output_callback(line.rstrip('\n'))
else:
    if self.error_callback:
        self.error_callback("Failed to capture process output")
```

### 9. Missing Widget Type Validation in Tab Data Driven
**File:** `src/ui/tab_data_driven.py` (lines 244-276)
**Status:** 🟢 Low
**Impact:** Could fail silently on unexpected control types

#### Solution
Add validation:
```python
def get_value(self, key: str):
    control = self.controls.get(key)
    if not control:
        return None

    control_type = control.get("type")
    widget = control.get("widget")

    if not control_type or not widget:
        return None

    # ... rest of logic with proper type checking
```

### 10. Type Validation in Tab Basic
**File:** `src/ui/tab_basic_improved.py` (line 352)
**Status:** 🟢 Low
**Impact:** Potential type error on edge cases

#### Solution
Add explicit type check:
```python
path = self.widgets['input_file'].get_path()

if not path or not isinstance(path, str):
    self.input_validation.setText("")
    self.input_validation.setStyleSheet("")
elif os.path.exists(path) and path.endswith('.py'):
    self.input_validation.setText("✓")
```

### 11. JSON Error Handling in Config Load
**File:** `src/core/config.py` (lines 208-209)
**Status:** 🟢 Low
**Impact:** Generic error message for JSON errors

#### Solution
```python
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        loaded_config = json.load(f)
except FileNotFoundError:
    return False, f"Configuration file not found: {filepath}"
except json.JSONDecodeError as e:
    return False, f"Invalid JSON in configuration file: {e}"
except IOError as e:
    return False, f"Cannot read configuration file: {e}"
```

---

## Implementation Strategy

### Phase 1: Critical Fixes (Immediate)
1. Fix `populate_artifacts()` error handling
2. Fix `setting_definitions.py` loader
3. Test application startup and artifact display

### Phase 2: High Priority (Week 1)
1. Move imports to module level in `tab_data.py`
2. Replace generic exceptions in `platform_detector.py`
3. Add comprehensive tests for platform detection

### Phase 3: Medium Priority (Week 2)
1. Implement proper error feedback mechanism (Qt signals)
2. Replace all print statements with UI feedback
3. Refactor exception handling in `config.py`
4. Improve error handling in `executor.py`

### Phase 4: Low Priority (Week 3)
1. Add defensive programming checks
2. Improve type validation
3. Add unit tests for edge cases
4. Code review and cleanup

### Phase 5: Testing & Documentation (Week 4)
1. Comprehensive testing on all platforms (Windows, macOS, Linux)
2. Update documentation
3. Add error handling guidelines for contributors
4. Create automated tests for bug scenarios

---

## Testing Checklist

After implementing fixes, verify:

- [ ] Application starts without errors
- [ ] Configuration files load properly
- [ ] Invalid configurations show user-friendly errors
- [ ] File operations handle permission errors gracefully
- [ ] Compilation process handles errors correctly
- [ ] UI feedback works for all error scenarios
- [ ] No console print statements remain (except debugging)
- [ ] All file paths are validated before use
- [ ] Platform-specific features work correctly
- [ ] Application handles missing dependencies gracefully

---

## Additional Improvements

While fixing bugs, consider these enhancements:

1. **Logging System**: Implement proper logging instead of print statements
2. **Error Dialog**: Create a reusable error dialog component
3. **Validation Framework**: Build a consistent validation system
4. **Unit Tests**: Add tests for all core modules
5. **Integration Tests**: Test full compilation workflows
6. **Documentation**: Add docstrings for error scenarios

---

## Notes

- All fixes should maintain backward compatibility
- Test each fix in isolation before moving to the next
- Document any API changes in the commit messages
- Consider creating a changelog for version tracking

---

**Last Updated:** 2026-01-15
**Status:** Ready for implementation

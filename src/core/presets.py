"""
Preset definitions and application.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class PresetDefinition:
    name: str
    description: str
    applies: List[Tuple[str, object]]


PRESETS: List[PresetDefinition] = [
    PresetDefinition(
        name="Standalone GUI App (recommended)",
        description="Standalone app with no console window.",
        applies=[
            ("basic.mode", "standalone"),
            ("modules.follow_imports", True),
            ("output.show_progress", True),
            ("platform.windows.console_mode", "disable"),
        ],
    ),
    PresetDefinition(
        name="CLI Tool (console on)",
        description="Standalone CLI build with console.",
        applies=[
            ("basic.mode", "standalone"),
            ("modules.follow_imports", True),
            ("platform.windows.console_mode", "force"),
        ],
    ),
    PresetDefinition(
        name="Onefile Distribution",
        description="Single-file distribution.",
        applies=[
            ("basic.mode", "onefile"),
            ("modules.follow_imports", True),
            ("output.show_progress", True),
        ],
    ),
    PresetDefinition(
        name="Debug / Trace Build",
        description="Verbose debug instrumentation.",
        applies=[
            ("advanced.debug", True),
            ("advanced.trace_execution", True),
            ("advanced.unstripped", True),
        ],
    ),
    PresetDefinition(
        name="Minimal Size",
        description="Aggressive size reduction.",
        applies=[
            ("advanced.lto", "yes"),
            ("output.show_progress", False),
            ("output.quiet", True),
        ],
    ),
    PresetDefinition(
        name="Max Compatibility",
        description="Max compatibility settings.",
        applies=[
            ("advanced.full_compat", True),
            ("modules.follow_stdlib", True),
            ("advanced.static_libpython", False),
        ],
    ),
]


def get_preset(name: str) -> Optional[PresetDefinition]:
    for preset in PRESETS:
        if preset.name == name:
            return preset
    return None


def apply_preset(config, preset: PresetDefinition) -> List[Tuple[str, object, object]]:
    changes = []
    for key, value in preset.applies:
        old_value = config.get(key)
        if old_value != value:
            config.set(key, value)
            changes.append((key, old_value, value))
    return changes

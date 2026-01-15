"""
Load data-driven setting definitions for the Nuitka GUI.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SettingDefinition:
    key: str
    label: str
    description: str
    effect: str
    risk: str
    impact: List[str]
    control: Dict[str, object]
    flag_mapping: List[Dict[str, object]]
    tab_id: str
    section_id: str
    section_title: str
    platform_constraints: Optional[Dict[str, List[str]]] = None


class SettingRegistry:
    def __init__(self, data: Dict[str, object]):
        self._tabs = data.get("tabs", [])
        self._by_key: Dict[str, SettingDefinition] = {}
        self._by_tab: Dict[str, List[SettingDefinition]] = {}
        self._load()

    def _load(self):
        for tab in self._tabs:
            tab_id = tab.get("id", "")
            sections = tab.get("sections", [])
            for section in sections:
                section_id = section.get("id", "")
                section_title = section.get("title", "")
                for setting in section.get("settings", []):
                    definition = SettingDefinition(
                        key=setting.get("key", ""),
                        label=setting.get("label", ""),
                        description=setting.get("description", ""),
                        effect=setting.get("effect", ""),
                        risk=setting.get("risk", "safe"),
                        impact=setting.get("impact", []),
                        control=setting.get("control", {}),
                        flag_mapping=setting.get("flag_mapping", []),
                        tab_id=tab_id,
                        section_id=section_id,
                        section_title=section_title,
                        platform_constraints=setting.get("platform_constraints"),
                    )
                    self._by_key[definition.key] = definition
                    self._by_tab.setdefault(tab_id, []).append(definition)

    def get_tabs(self) -> List[Dict[str, object]]:
        return list(self._tabs)

    def get_setting(self, key: str) -> Optional[SettingDefinition]:
        return self._by_key.get(key)

    def get_tab_settings(self, tab_id: str) -> List[SettingDefinition]:
        return self._by_tab.get(tab_id, [])

    def get_all_settings(self) -> List[SettingDefinition]:
        return list(self._by_key.values())


_registry_cache: Optional[SettingRegistry] = None


def get_definitions_path() -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "setting_definitions.json"


def load_setting_definitions(path: Optional[Path] = None) -> SettingRegistry:
    global _registry_cache
    if _registry_cache is not None and path is None:
        return _registry_cache

    target = path or get_definitions_path()
    with target.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    registry = SettingRegistry(data)
    if path is None:
        _registry_cache = registry
    return registry

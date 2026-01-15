"""
Flag plan compilation and rendering.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .setting_definitions import SettingRegistry


GROUP_ORDER = [
    "mode",
    "output",
    "imports",
    "data",
    "platform",
    "opt",
    "compat",
    "debug",
    "runtime",
    "plugins",
    "misc",
]


@dataclass(frozen=True)
class FlagAtom:
    id: str
    args: Tuple[str, ...]
    sources: Tuple[str, ...]
    group: str


@dataclass
class FlagPlan:
    flags: List[FlagAtom] = field(default_factory=list)
    entry_script: Optional[str] = None


def _get_value(settings: Dict[str, object], dotted_key: str):
    value = settings
    for part in dotted_key.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None
    return value


def _normalize_flag(flag: str) -> str:
    return flag.strip()


def _add_atom(
    atoms: List[FlagAtom],
    flag_id: str,
    arg: str,
    sources: List[str],
    group: str,
):
    atoms.append(
        FlagAtom(
            id=flag_id,
            args=(arg,),
            sources=tuple(sorted(set(sources))),
            group=group or "misc",
        )
    )


def _handle_compiler(settings: Dict[str, object], atoms: List[FlagAtom], group: str, key: str):
    compiler = _get_value(settings, key) or "auto"
    if compiler == "auto":
        return
    if compiler == "msvc":
        msvc_version = _get_value(settings, "basic.msvc_version") or "latest"
        _add_atom(atoms, "msvc", f"--msvc={msvc_version}", [key], group)
        return
    mapping = {
        "mingw64": "--mingw64",
        "clang": "--clang",
        "zig": "--zig",
    }
    flag = mapping.get(compiler)
    if flag:
        _add_atom(atoms, compiler, flag, [key], group)


def _handle_progress(settings: Dict[str, object], atoms: List[FlagAtom], group: str):
    show_progress = _get_value(settings, "output.show_progress")
    progress_mode = _get_value(settings, "output.progress_mode") or "auto"
    if show_progress is False:
        _add_atom(atoms, "no_progressbar", "--no-progressbar", ["output.show_progress"], group)
        return
    if show_progress is True and progress_mode and progress_mode != "auto":
        _add_atom(
            atoms,
            "progress_bar",
            f"--progress-bar={progress_mode}",
            ["output.show_progress", "output.progress_mode"],
            group,
        )


def compile_flag_plan(settings: Dict[str, object], registry: SettingRegistry) -> FlagPlan:
    atoms: List[FlagAtom] = []
    entry_script = _get_value(settings, "basic.input_file")

    for definition in registry.get_all_settings():
        value = _get_value(settings, definition.key)
        for mapping in definition.flag_mapping:
            mapping_type = mapping.get("type")
            group = mapping.get("group", "misc")
            map_id = mapping.get("id") or mapping.get("flag") or definition.key

            if mapping_type == "compiler":
                _handle_compiler(settings, atoms, group, definition.key)
                continue
            if mapping_type == "progress":
                _handle_progress(settings, atoms, group)
                continue

            if mapping_type == "flag_bool":
                flag = mapping.get("flag")
                else_flag = mapping.get("else_flag")
                if value is True and flag:
                    _add_atom(atoms, map_id, _normalize_flag(flag), [definition.key], group)
                elif value is False and else_flag:
                    _add_atom(atoms, map_id, _normalize_flag(else_flag), [definition.key], group)
                continue

            if mapping_type == "flag_value":
                if value is None or value == "":
                    continue
                omit_if = mapping.get("omit_if", [])
                if value in omit_if:
                    continue
                flag = mapping.get("flag")
                if flag:
                    _add_atom(atoms, map_id, f"{_normalize_flag(flag)}{value}", [definition.key], group)
                continue

            if mapping_type == "flag_list":
                if not value:
                    continue
                flag = mapping.get("flag")
                if flag:
                    for item in value:
                        if item is None or item == "":
                            continue
                        item_id = f"{map_id}:{item}"
                        _add_atom(atoms, item_id, f"{_normalize_flag(flag)}{item}", [definition.key], group)
                continue

            if mapping_type == "flag_join":
                if not value:
                    continue
                flag = mapping.get("flag")
                if flag:
                    joined = ",".join([str(v) for v in value if v])
                    if joined:
                        _add_atom(atoms, map_id, f"{_normalize_flag(flag)}{joined}", [definition.key], group)
                continue

    return FlagPlan(flags=atoms, entry_script=entry_script)


def render_command(plan: FlagPlan, python_exe: Optional[str] = None) -> List[str]:
    args = [python_exe or "python", "-m", "nuitka"]

    group_index = {name: idx for idx, name in enumerate(GROUP_ORDER)}
    plan.flags.sort(key=lambda atom: (group_index.get(atom.group, 99), atom.id))

    for atom in plan.flags:
        args.extend(atom.args)

    if plan.entry_script:
        args.append(plan.entry_script)

    return args


def render_command_string(plan: FlagPlan, python_exe: Optional[str] = None) -> str:
    args = render_command(plan, python_exe=python_exe)
    quoted = []
    for arg in args:
        if " " in arg and not (arg.startswith('"') and arg.endswith('"')):
            quoted.append(f'"{arg}"')
        else:
            quoted.append(arg)
    return " ".join(quoted)

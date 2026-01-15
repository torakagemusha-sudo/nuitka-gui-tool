"""
Semantic diff for FlagPlan.
"""
from __future__ import annotations

from typing import Dict, List

from .flag_plan import FlagPlan


def _index(plan: FlagPlan) -> Dict[str, Dict[str, object]]:
    result = {}
    for atom in plan.flags:
        result[atom.id] = {
            "args": atom.args,
            "sources": atom.sources,
            "group": atom.group,
        }
    return result


def diff_flag_plans(plan_a: FlagPlan, plan_b: FlagPlan) -> Dict[str, List[str]]:
    a = _index(plan_a)
    b = _index(plan_b)

    added = [key for key in b.keys() if key not in a]
    removed = [key for key in a.keys() if key not in b]
    changed = []
    provenance_changed = []

    for key in a.keys() & b.keys():
        if a[key]["args"] != b[key]["args"]:
            changed.append(key)
        elif a[key]["sources"] != b[key]["sources"]:
            provenance_changed.append(key)

    return {
        "added": sorted(added),
        "removed": sorted(removed),
        "changed": sorted(changed),
        "provenance_changed": sorted(provenance_changed),
    }

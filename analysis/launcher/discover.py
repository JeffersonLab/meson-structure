"""Find analysis folders that opt into the launcher.

A folder participates iff it contains BOTH `runner.py` and `meta.yaml`.
"""
from __future__ import annotations

from pathlib import Path


def discover_analyses(analysis_root: Path) -> list[str]:
    """Return sorted folder names under `analysis_root` that have a runner+meta."""
    if not analysis_root.is_dir():
        return []
    names: list[str] = []
    for child in sorted(analysis_root.iterdir()):
        if not child.is_dir() or child.name.startswith((".", "_")):
            continue
        if (child / "runner.py").is_file() and (child / "meta.yaml").is_file():
            names.append(child.name)
    return names

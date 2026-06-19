"""Repository path discovery, computed once.

Modules that need to read or write files at known repo locations import from here so the
layout is described in exactly one file.
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "PACKAGE_ROOT",
    "MODEL_ROOT",
    "REPO_ROOT",
    "DATA_DIR",
    "ASSETS",
    "REPORT",
    "GRANTS",
]


PACKAGE_ROOT: Path = Path(__file__).resolve().parent
MODEL_ROOT: Path = PACKAGE_ROOT.parent.parent
REPO_ROOT: Path = MODEL_ROOT.parent

DATA_DIR: Path = MODEL_ROOT / "data"
ASSETS: Path = REPO_ROOT / "deck" / "assets"
REPORT: Path = REPO_ROOT / "report"
GRANTS: Path = REPO_ROOT / "grants"

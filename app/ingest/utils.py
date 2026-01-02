from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTS = {".md", ".txt", ".pdf"}


def stable_id(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in SUPPORTED_EXTS:
            yield root
        return

    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            yield p

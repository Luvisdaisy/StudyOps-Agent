from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pypdf import PdfReader

from app.ingest.types import Document
from app.ingest.utils import stable_id


class Loader(Protocol):
    def load(self, path: Path) -> Document: ...


@dataclass(frozen=True)
class TextLoader:
    encoding: str = "utf-8"

    def load(self, path: Path) -> Document:
        text = path.read_text(encoding=self.encoding, errors="ignore")
        doc_id = stable_id(str(path.resolve()))
        return Document(
            doc_id=doc_id,
            text=text,
            metadata={
                "source_path": str(path.resolve()),
                "ext": path.suffix.lower(),
                "name": path.name,
            },
        )


@dataclass(frozen=True)
class PdfLoader:
    def load(self, path: Path) -> Document:
        reader = PdfReader(str(path))
        pages = []
        for i, page in enumerate(reader.pages):
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n\n".join(pages)
        doc_id = stable_id(str(path.resolve()))
        return Document(
            doc_id=doc_id,
            text=text,
            metadata={
                "source_path": str(path.resolve()),
                "ext": path.suffix.lower(),
                "name": path.name,
                "pages": len(reader.pages),
            },
        )


def get_loader(path: Path) -> Loader:
    ext = path.suffix.lower()
    if ext in {".md", ".txt"}:
        return TextLoader()
    if ext == ".pdf":
        return PdfLoader()
    raise ValueError(f"Unsupported file type: {ext}")

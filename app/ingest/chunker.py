from __future__ import annotations

from dataclasses import dataclass

from app.ingest.types import Chunk, Document
from app.ingest.utils import stable_id


@dataclass(frozen=True)
class ChunkConfig:
    max_chars: int = 1200
    overlap: int = 150


def chunk_text(text: str, max_chars: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        # move start forward with overlap
        start = max(0, end - overlap)

    return chunks


def chunk_document(doc: Document, cfg: ChunkConfig) -> list[Chunk]:
    parts = chunk_text(doc.text, cfg.max_chars, cfg.overlap)
    out: list[Chunk] = []
    for idx, part in enumerate(parts):
        chunk_id = stable_id(f"{doc.doc_id}:{idx}:{len(part)}")
        out.append(
            Chunk(
                chunk_id=chunk_id,
                doc_id=doc.doc_id,
                text=part,
                metadata={**doc.metadata, "chunk_index": idx},
            )
        )
    return out

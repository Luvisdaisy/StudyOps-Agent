from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.ingest.chunker import ChunkConfig, chunk_document
from app.ingest.loaders import get_loader
from app.ingest.utils import iter_files
from app.storage.chroma_store import ChromaStore, ChromaConfig


@dataclass(frozen=True)
class IngestResult:
    files_total: int
    docs_ok: int
    docs_skipped: int
    chunks_written: int


def ingest_path(
    path: str | Path,
    chroma_cfg: ChromaConfig,
    chunk_cfg: ChunkConfig,
) -> IngestResult:
    root = Path(path).expanduser().resolve()

    store = ChromaStore(chroma_cfg)

    files = list(iter_files(root))
    docs_ok = 0
    docs_skipped = 0
    chunks_written = 0

    for f in files:
        try:
            loader = get_loader(f)
            doc = loader.load(f)
            if not doc.text.strip():
                docs_skipped += 1
                continue

            chunks = chunk_document(doc, chunk_cfg)
            store.upsert_chunks(chunks)

            docs_ok += 1
            chunks_written += len(chunks)
        except Exception:
            docs_skipped += 1

    return IngestResult(
        files_total=len(files),
        docs_ok=docs_ok,
        docs_skipped=docs_skipped,
        chunks_written=chunks_written,
    )

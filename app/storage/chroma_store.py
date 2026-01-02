from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import chromadb
from chromadb.config import Settings

from app.ingest.types import Chunk


@dataclass(frozen=True)
class ChromaConfig:
    persist_dir: str
    collection: str


class ChromaStore:
    def __init__(self, cfg: ChromaConfig) -> None:
        """
        Compatible with both:
        - New Chroma: chromadb.PersistentClient(path=...)
        - Old Chroma: chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=...))
        """
        self._cfg = cfg

        if hasattr(chromadb, "PersistentClient"):
            # Newer API
            self._client = chromadb.PersistentClient(
                path=cfg.persist_dir,
                settings=Settings(anonymized_telemetry=False),
            )
        else:
            # Older API
            self._client = chromadb.Client(
                Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=cfg.persist_dir,
                    anonymized_telemetry=False,
                )
            )

        self._col = self._client.get_or_create_collection(name=cfg.collection)

    def upsert_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return

        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas: list[dict[str, Any]] = [c.metadata for c in chunks]

        self._col.upsert(ids=ids, documents=documents, metadatas=metadatas)

        # Old Chroma requires explicit persist
        if hasattr(self._client, "persist"):
            self._client.persist()

    def count(self) -> int:
        return self._col.count()

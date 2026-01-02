from __future__ import annotations

import typer

app = typer.Typer(
    help="StudyOps Agent - local CLI entry",
    add_completion=False,
)

@app.command()
def health(config: str = typer.Option("configs/app.toml", help="Path to config file")) -> None:
    """
    Check local dependencies (Redis / Neo4j) connectivity.
    """
    from app.utils.config import load_config
    from redis import Redis
    from neo4j import GraphDatabase

    cfg = load_config(config)

    # Redis check
    try:
        r = Redis.from_url(cfg.redis.url)
        pong = r.ping()
        typer.echo(f"Redis: OK (ping={pong})")
    except Exception as e:
        typer.echo(f"Redis: FAIL ({e})")

    # Neo4j check
    try:
        driver = GraphDatabase.driver(cfg.neo4j.uri, auth=(cfg.neo4j.user, cfg.neo4j.password))
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok").single()
            typer.echo(f"Neo4j: OK (RETURN {result['ok']})")
        driver.close()
    except Exception as e:
        typer.echo(f"Neo4j: FAIL ({e})")



@app.command()
def ingest(
    path: str,
    config: str = typer.Option("configs/app.toml", help="Path to config file"),
) -> None:
    """
    Ingest documents from a directory (md/txt/pdf), chunk them, and store in Chroma.
    """
    from app.utils.config import load_config
    from app.ingest.pipeline import ingest_path
    from app.storage.chroma_store import ChromaConfig as StoreChromaConfig
    from app.ingest.chunker import ChunkConfig as IngestChunkConfig

    cfg = load_config(config)

    result = ingest_path(
        path=path,
        chroma_cfg=StoreChromaConfig(
            persist_dir=cfg.chroma.persist_dir,
            collection=cfg.chroma.collection,
        ),
        chunk_cfg=IngestChunkConfig(
            max_chars=cfg.chunk.max_chars,
            overlap=cfg.chunk.overlap,
        ),
    )

    typer.echo("Ingest done.")
    typer.echo(f"- Files found:    {result.files_total}")
    typer.echo(f"- Docs ingested:  {result.docs_ok}")
    typer.echo(f"- Docs skipped:   {result.docs_skipped}")
    typer.echo(f"- Chunks written: {result.chunks_written}")



@app.command()
def chat() -> None:
    """
    Placeholder for chat loop.
    """
    typer.echo("[TODO] chat mode")


@app.command("graph-build")
def graph_build() -> None:
    """
    Placeholder for graph build pipeline.
    """
    typer.echo("[TODO] graph build")


@app.command("graph-query")
def graph_query(q: str) -> None:
    """
    Placeholder for graph query.
    """
    typer.echo(f"[TODO] graph query: {q}")

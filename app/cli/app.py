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
def ingest(path: str) -> None:
    """
    Placeholder for ingestion pipeline.
    """
    typer.echo(f"[TODO] ingest from: {path}")


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

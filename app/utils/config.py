from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class RedisConfig:
    url: str


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    user: str
    password: str


@dataclass(frozen=True)
class AppConfig:
    redis: RedisConfig
    neo4j: Neo4jConfig


def load_config(path: str | Path = "configs/app.toml") -> AppConfig:
    p = Path(path)
    data = tomllib.loads(p.read_text(encoding="utf-8"))

    redis = data["redis"]
    neo4j = data["neo4j"]

    return AppConfig(
        redis=RedisConfig(url=redis["url"]),
        neo4j=Neo4jConfig(uri=neo4j["uri"], user=neo4j["user"], password=neo4j["password"]),
    )

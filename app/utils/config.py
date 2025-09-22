from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8001"))
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "local-dummy")
    vector_dir: str = os.getenv("VECTOR_DIR", "gpt5-child/vector_store/simple_index")


from __future__ import annotations
import json, time
from pathlib import Path
from typing import Dict, Any


class ExperienceBuffer:
    def __init__(self, path: str | None = None):
        self.path = Path(path or "gpt5-child/data/experience.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: Dict[str, Any]) -> None:
        rec = {"ts": time.time(), **event}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


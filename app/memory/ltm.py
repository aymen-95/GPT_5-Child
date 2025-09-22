from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np


class SimpleVectorStore:
    def __init__(self, directory: Path | None = None):
        self.dir = directory or Path("gpt5-child/vector_store/simple_index")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.emb_path = self.dir / "embeddings.npy"
        self.meta_path = self.dir / "meta.jsonl"
        self._emb: np.ndarray = np.zeros((0, 0), dtype=np.float32)
        self._meta: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.emb_path.exists():
            self._emb = np.load(self.emb_path)
        if self.meta_path.exists():
            with self.meta_path.open("r", encoding="utf-8") as f:
                self._meta = [json.loads(line) for line in f if line.strip()]

    def _save(self) -> None:
        if self._emb is not None:
            np.save(self.emb_path, self._emb)
        with self.meta_path.open("w", encoding="utf-8") as f:
            for m in self._meta:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def add(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
        if self._emb.size == 0:
            self._emb = embeddings.astype(np.float32)
        else:
            if self._emb.shape[1] != embeddings.shape[1]:
                raise ValueError("embedding dim mismatch")
            self._emb = np.vstack([self._emb, embeddings.astype(np.float32)])
        self._meta.extend(metadatas)
        self._save()

    def query(self, q: np.ndarray, top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        if self._emb.size == 0:
            return []
        q = q.reshape(1, -1)
        q = q / (np.linalg.norm(q) + 1e-9)
        m = self._emb
        m_norm = m / (np.linalg.norm(m, axis=1, keepdims=True) + 1e-9)
        sims = (m_norm @ q.T).ravel()
        idx = np.argsort(-sims)[:top_k]
        return [(float(sims[i]), self._meta[i]) for i in idx]


from __future__ import annotations
import hashlib
import numpy as np
from typing import List


class EmbeddingBackend:
    def __init__(self, model_name: str | None = None, dim: int = 384):
        self.model_name = model_name or "local-dummy"
        self.dim = dim

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        arr = np.zeros((len(texts), self.dim), dtype=np.float32)
        for i, t in enumerate(texts):
            for tok in t.lower().split():
                h = int(hashlib.sha1(tok.encode()).hexdigest(), 16)
                idx = h % self.dim
                arr[i, idx] += 1.0
            n = np.linalg.norm(arr[i]) + 1e-9
            arr[i] /= n
        return arr


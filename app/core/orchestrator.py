from __future__ import annotations
from typing import Dict, Any
from app.inference.llm import generate
from app.memory.stm import STM
from app.memory.ltm import SimpleVectorStore
from app.memory.embeddings import EmbeddingBackend
from app.core.safety import safe_guard


class Orchestrator:
    def __init__(self):
        self.stm = STM()
        self.emb = EmbeddingBackend()
        self.ltm = SimpleVectorStore()

    def handle(self, task: str) -> Dict[str, Any]:
        # naive intent and retrieval
        ctx = []
        try:
            qv = self.emb.embed_texts([task])[0]
            res = self.ltm.query(qv, top_k=5)
            ctx = [{"text": m.get("text", ""), "score": s} for s, m in res]
        except Exception:
            ctx = []
        prompt = self._build_prompt(task, ctx)
        prompt = safe_guard(prompt)
        ans = generate(prompt)
        self.stm.put("last_answer", ans)
        return {"answer": ans, "contexts": ctx}

    @staticmethod
    def _build_prompt(task: str, contexts: list[dict]) -> str:
        parts = ["Task:\n", task, "\n\nContexts:\n"]
        for i, c in enumerate(contexts, 1):
            parts.append(f"[{i}] score={c.get('score',0):.3f}\n{c.get('text','')}\n\n")
        parts.append("Answer:\n")
        return "".join(parts)


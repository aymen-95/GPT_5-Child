from __future__ import annotations
import glob
from pathlib import Path
from typing import Dict, Any, List
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.memory.ltm import SimpleVectorStore
from app.memory.embeddings import EmbeddingBackend


router = APIRouter()
EMB = EmbeddingBackend()
STORE = SimpleVectorStore(Path("gpt5-child/vector_store/simple_index"))


class IngestDirRequest(BaseModel):
    path: str
    recursive: bool = Field(default=True)
    glob: str = Field(default="*.txt,*.md")
    tag: str = Field(default="bootstrap")


class IngestItemRequest(BaseModel):
    text: str
    meta: Dict[str, Any] = Field(default_factory=dict)


class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5)


@router.post("/ingest_directory")
def ingest_directory(req: IngestDirRequest) -> Dict[str, Any]:
    root = Path(req.path)
    pats = [p.strip() for p in req.glob.split(",") if p.strip()]
    files: List[Path] = []
    for pat in pats:
        files += [Path(p) for p in glob.glob(str(root / ("**/" + pat)), recursive=req.recursive)]
    added = 0
    for fp in files:
        try:
            txt = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        chunks = [txt] if len(txt.split()) < 800 else [txt]  # simple stub
        texts = chunks
        embs = EMB.embed_texts(texts)
        meta = [{"text": t, "source": str(fp), "tag": req.tag} for t in texts]
        STORE.add(embs, meta)
        added += len(texts)
    return {"status": "ok", "files": len(files), "chunks": added}


@router.post("/item")
def ingest_item(req: IngestItemRequest) -> Dict[str, Any]:
    embs = EMB.embed_texts([req.text])
    meta = [{"text": req.text, **req.meta}]
    STORE.add(embs, meta)
    return {"status": "ok", "chunks": 1}


@router.post("/query")
def query(req: QueryRequest) -> Dict[str, Any]:
    q = EMB.embed_texts([req.query])[0]
    res = STORE.query(q, top_k=req.top_k)
    return {"results": [{"score": s, **m} for s, m in res]}


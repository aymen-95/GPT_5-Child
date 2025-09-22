from __future__ import annotations
import argparse, glob
from pathlib import Path
from app.memory.embeddings import EmbeddingBackend
from app.memory.ltm import SimpleVectorStore


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Ingest a folder into LTM vector store")
    p.add_argument("--path", required=True)
    p.add_argument("--recursive", default="true")
    p.add_argument("--glob", default="*.txt,*.md")
    p.add_argument("--tag", default="bootstrap")
    args = p.parse_args(argv)

    emb = EmbeddingBackend()
    store = SimpleVectorStore()

    root = Path(args.path)
    pats = [s.strip() for s in args.glob.split(",") if s.strip()]
    files = []
    for pat in pats:
        files += glob.glob(str(root / ("**/" + pat)), recursive=(args.recursive.lower()=="true"))

    added = 0
    for fp in files:
        try:
            txt = Path(fp).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        texts = [txt]
        embs = emb.embed_texts(texts)
        meta = [{"text": t, "source": fp, "tag": args.tag} for t in texts]
        store.add(embs, meta)
        added += len(texts)
    print(f"files={len(files)} chunks={added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


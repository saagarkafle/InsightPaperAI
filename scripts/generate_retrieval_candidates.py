#!/usr/bin/env python3
"""
Generate top-K retrieval candidates (chunk previews) for each eval query.

Outputs `data/eval_candidates.jsonl` with one JSON object per query:
{
  "id": "q1",
  "query": "...",
  "top_k": [ {"chunk_index": 12, "score": 0.823, "preview": "first 300 chars"}, ... ]
}
"""
import argparse
import json
from pathlib import Path

import numpy as np

from src.pdf_parser import extract_text_from_pdf
from src.rag_pipeline import chunk_text, embed_query, embed_texts, get_embedder


def cosine_sim(a: np.ndarray, b: np.ndarray):
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    sims = (a @ b) / (a_norm.flatten() * b_norm + 1e-12)
    return sims


def run(args):
    eval_path = Path(args.eval_file)
    out_path = Path("data/eval_candidates.jsonl")
    embedder = get_embedder()

    results = []
    with eval_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            qid = rec.get("id")
            query = rec.get("query")

            # Load text
            text = None
            if rec.get("pdf"):
                p = Path(rec.get("pdf"))
                if not p.exists():
                    print(f"Skipping {qid}: pdf not found {p}")
                    continue
                with p.open("rb") as fh:
                    pdf_bytes = fh.read()
                text = extract_text_from_pdf(pdf_bytes)
            elif rec.get("text_file"):
                tpath = Path(rec.get("text_file"))
                if not tpath.exists():
                    print(f"Skipping {qid}: text_file not found {tpath}")
                    continue
                text = tpath.read_text(encoding="utf-8")
            else:
                print(f"Skipping {qid}: no pdf/text_file provided")
                continue

            chunks = chunk_text(
                text, chunk_size=args.chunk_size, overlap=args.overlap)
            if not chunks:
                print(f"No chunks for {qid}")
                continue

            vecs = np.array(embed_texts(chunks, embedder))
            qvec = np.array(embed_query(query, embedder))
            sims = cosine_sim(vecs, qvec)
            idx_sort = list(np.argsort(-sims))
            top_idx = idx_sort[: args.top_k]

            top_k_list = []
            for idx in top_idx:
                top_k_list.append({
                    "chunk_index": int(idx),
                    "score": float(sims[idx]),
                    "preview": chunks[idx][:300].replace('\n', ' ')
                })

            out = {"id": qid, "query": query, "top_k": top_k_list}
            results.append(out)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fo:
        for r in results:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(results)} candidate entries to {out_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("eval_file", default="data/eval.jsonl", nargs="?")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--chunk-size", type=int, default=500)
    p.add_argument("--overlap", type=int, default=100)
    args = p.parse_args()
    run(args)

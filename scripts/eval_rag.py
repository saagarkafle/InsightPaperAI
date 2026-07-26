#!/usr/bin/env python3
"""
scripts/eval_rag.py — Evaluate RAG retrieval and QA performance.

Supports two evaluation modes:

  1. Per-document mode: Each eval record points to a PDF, text file, or inline
     context. Chunks are created per document and retrieval is evaluated within
     each document independently.

  2. Corpus-wide mode (auto-detected): When all records have inline "context"
     fields, all documents are pooled into a single corpus. Retrieval is
     evaluated by checking whether each query retrieves chunks belonging to
     its source document from the full corpus — a harder, more realistic test.

Input format (JSONL, one record per line):
  {
    "id": "q1",
    "query": "What is the main method?",
    "pdf": "path/to/paper.pdf",           # optional
    "text_file": "path/to/text.txt",       # optional
    "context": "inline text...",            # optional
    "relevant_chunk_indices": [2, 5],       # optional
    "gold_answers": ["We propose X ..."]    # optional, for QA metrics
  }

Usage:
  python scripts/eval_rag.py data/kaggle_eval.jsonl --mode local --top-k 5
  python scripts/eval_rag.py data/kaggle_eval.jsonl --mode local --embedder-model all-MiniLM-L6-v2
  python scripts/eval_rag.py data/eval.jsonl --mode local --call-llm --top-k 5
"""
import argparse
import time
from pathlib import Path
from statistics import mean

import numpy as np

from src.llm_qa import answer_question, get_groq_client
from src.pdf_parser import extract_text_from_pdf
from src.rag_pipeline import chunk_text, embed_query, embed_texts, get_embedder

# ── Text Metrics ─────────────────────────────────────────────────────────────

import json
import re


def _normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())


def exact_match(pred: str, gold: str) -> int:
    return int(_normalize(pred) == _normalize(gold))


def f1_score(pred: str, gold: str) -> float:
    p_tokens = _normalize(pred).split()
    g_tokens = _normalize(gold).split()
    if not p_tokens or not g_tokens:
        return float(p_tokens == g_tokens)
    common = sum(min(p_tokens.count(t), g_tokens.count(t)) for t in set(p_tokens))
    if common == 0:
        return 0.0
    prec = common / len(p_tokens)
    rec = common / len(g_tokens)
    return 2 * prec * rec / (prec + rec)


# ── Retrieval Metrics ────────────────────────────────────────────────────────

def recall_at_k(preds, gold_set, k):
    return 1.0 if any(p in gold_set for p in preds[:k]) else 0.0


def reciprocal_rank(preds, gold_set):
    for i, p in enumerate(preds, start=1):
        if p in gold_set:
            return 1.0 / i
    return 0.0


def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    return (a @ b) / (a_norm.flatten() * b_norm + 1e-12)


# ── Data Loading ─────────────────────────────────────────────────────────────

def load_eval(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def run_local_retrieval(chunks, query, embedder, top_k=5):
    vecs = np.array(embed_texts(chunks, embedder))
    qvec = np.array(embed_query(query, embedder))
    sims = cosine_sim(vecs, qvec)
    idx_sort = list(np.argsort(-sims))
    top_idx = idx_sort[:top_k]
    top_scores = [float(sims[i]) for i in top_idx]
    return top_idx, top_scores


# ── LLM QA Helper ───────────────────────────────────────────────────────────

def _call_llm(query, chunks_for_llm, groq_client, model_override):
    """Call the LLM for a QA answer and return the predicted text."""
    if model_override:
        resp = answer_question(query, chunks_for_llm, client=groq_client, model=model_override)
    else:
        resp = answer_question(query, chunks_for_llm, client=groq_client)
    return resp.answer.strip()


def _score_qa(pred: str, gold_answers: list[str], em_scores, f1_scores):
    """Compute and append EM/F1 scores if gold answers are provided."""
    if gold_answers:
        em_scores.append(max(exact_match(pred, g) for g in gold_answers))
        f1_scores.append(max(f1_score(pred, g) for g in gold_answers))


# ── Corpus-Wide Evaluation ───────────────────────────────────────────────────

def _eval_corpus_wide(records, embedder, args, groq_client,
                      retrieval_recalls, retrieval_rr,
                      em_scores, f1_scores, latencies):
    """Evaluate retrieval across a pooled corpus of inline context documents."""
    print(f"Detected {len(records)} inline context records. Running corpus-wide retrieval benchmark...")

    # Build corpus: chunk all documents and track which doc each chunk belongs to
    all_chunks = []
    doc_map = []  # chunk_index → document_index
    for doc_idx, rec in enumerate(records):
        chunks = chunk_text(str(rec["context"]),
                            chunk_size=args.chunk_size, overlap=args.overlap)
        for c in chunks:
            all_chunks.append(c)
            doc_map.append(doc_idx)

    corpus_vecs = np.array(embed_texts(all_chunks, embedder))

    for doc_idx, rec in enumerate(records):
        query = rec["query"]
        gold_answers = rec.get("gold_answers", [])

        qvec = np.array(embed_query(query, embedder))
        sims = cosine_sim(corpus_vecs, qvec)
        idx_sort = list(np.argsort(-sims))
        retrieved_doc_indices = [doc_map[i] for i in idx_sort[:args.top_k]]

        # Retrieval metric: is the source document in the top-k?
        retrieval_recalls.append(1.0 if doc_idx in retrieved_doc_indices else 0.0)
        rr = 0.0
        for rank_pos, d_idx in enumerate(retrieved_doc_indices, start=1):
            if d_idx == doc_idx:
                rr = 1.0 / rank_pos
                break
        retrieval_rr.append(rr)

        # Optional LLM QA
        if args.call_llm and groq_client is not None:
            top_chunks = [{
                "text": all_chunks[i],
                "score": float(sims[i]),
                "paper_title": records[doc_map[i]].get("title", f"doc_{doc_map[i]}"),
                "paper_id": records[doc_map[i]].get("id", ""),
                "chunk_index": int(i),
            } for i in idx_sort[:args.top_k]]

            start = time.time()
            try:
                pred = _call_llm(query, top_chunks, groq_client, args.model)
                latencies.append(time.time() - start)
            except Exception as e:
                print(f"LLM call failed for {rec.get('id')}: {e}")
                pred = ""
            _score_qa(pred, gold_answers, em_scores, f1_scores)


# ── Per-Document Evaluation ──────────────────────────────────────────────────

def _eval_per_document(records, embedder, args, groq_client,
                       retrieval_recalls, retrieval_rr,
                       em_scores, f1_scores, latencies):
    """Evaluate retrieval and QA per individual document."""
    for rec in records:
        qid = rec.get("id")
        query = rec.get("query")
        gold_answers = rec.get("gold_answers", [])
        gold_indices = set(rec.get("relevant_chunk_indices", []))

        # Load text from the appropriate source
        text = None
        if rec.get("pdf"):
            p = Path(rec["pdf"])
            if not p.exists():
                print(f"Skipping {qid}: pdf not found {p}")
                continue
            with p.open("rb") as f:
                text = extract_text_from_pdf(f.read())
        elif rec.get("text_file"):
            tpath = Path(rec["text_file"])
            if not tpath.exists():
                print(f"Skipping {qid}: text_file not found {tpath}")
                continue
            text = tpath.read_text(encoding="utf-8")
        elif rec.get("context"):
            text = str(rec["context"])
        else:
            print(f"Skipping {qid}: no pdf/text_file/context provided")
            continue

        chunks = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
        top_idx, top_scores = run_local_retrieval(chunks, query, embedder, top_k=args.top_k)

        # Retrieval metrics
        if gold_indices:
            retrieval_recalls.append(recall_at_k(top_idx, gold_indices, args.top_k))
            retrieval_rr.append(reciprocal_rank(top_idx, gold_indices))

        # Optional LLM QA
        if args.call_llm and groq_client is not None:
            retrieved_chunks = [{
                "text": chunks[idx],
                "score": float(top_scores[rank]) if rank < len(top_scores) else 0.0,
                "paper_title": rec.get("pdf", rec.get("text_file", "unknown")),
                "paper_id": rec.get("id", ""),
                "chunk_index": int(idx),
            } for rank, idx in enumerate(top_idx)]

            start = time.time()
            try:
                pred = _call_llm(query, retrieved_chunks, groq_client, args.model)
                latencies.append(time.time() - start)
            except Exception as e:
                print(f"LLM call failed for {qid}: {e}")
                pred = ""
            _score_qa(pred, gold_answers, em_scores, f1_scores)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Evaluate RAG retrieval and QA performance"
    )
    parser.add_argument("eval_file", help="Path to eval JSONL file")
    parser.add_argument("--mode", choices=["local", "pinecone"], default="local")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--call-llm", action="store_true", help="Call LLM for QA answers")
    parser.add_argument("--model", default=None, help="LLM model override")
    parser.add_argument(
        "--embedder-model", default=None,
        help="Embedder model path or name (e.g. all-MiniLM-L6-v2 or models/fine_tuned_embedder)",
    )
    args = parser.parse_args()

    eval_path = Path(args.eval_file)
    if not eval_path.exists():
        raise SystemExit(f"Eval file not found: {eval_path}")

    embedder = get_embedder(args.embedder_model)
    records = load_eval(eval_path)

    # Metric accumulators
    retrieval_recalls, retrieval_rr = [], []
    em_scores, f1_scores, latencies = [], [], []

    # Init LLM client if needed
    groq_client = None
    if args.call_llm:
        try:
            groq_client = get_groq_client()
        except Exception as e:
            print(f"Warning: could not init LLM client: {e}")

    # Choose evaluation strategy
    has_inline_contexts = all(
        rec.get("context") for rec in records
        if not rec.get("pdf") and not rec.get("text_file")
    )

    if has_inline_contexts and len(records) > 1:
        _eval_corpus_wide(
            records, embedder, args, groq_client,
            retrieval_recalls, retrieval_rr, em_scores, f1_scores, latencies,
        )
    else:
        _eval_per_document(
            records, embedder, args, groq_client,
            retrieval_recalls, retrieval_rr, em_scores, f1_scores, latencies,
        )

    # ── Print results ────────────────────────────────────────────────────────
    print("\nEvaluation results:\n")
    if retrieval_recalls:
        print(f"Retrieval recall@{args.top_k}: {mean(retrieval_recalls):.4f}")
        print(f"Retrieval MRR: {mean(retrieval_rr):.4f}")
    else:
        print("No retrieval labels provided; skipping retrieval metrics.")

    if em_scores:
        print(f"QA Exact Match: {mean(em_scores):.4f}")
        print(f"QA F1: {mean(f1_scores):.4f}")
        if latencies:
            print(f"Avg LLM latency: {mean(latencies):.2f}s")
    else:
        if args.call_llm:
            print("LLM was called but no gold answers found to compute QA metrics.")
        else:
            print("LLM not called; QA metrics skipped.")


if __name__ == "__main__":
    main()

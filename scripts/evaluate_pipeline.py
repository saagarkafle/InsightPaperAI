#!/usr/bin/env python3
"""
Evaluate the RAG pipeline locally: parsing, chunking, embedding, and local semantic search.

Usage examples:

python scripts/evaluate_pipeline.py --text-file path/to/text.txt --query "what is the method"
python scripts/evaluate_pipeline.py --pdf path/to/paper.pdf --query "experiment results"
"""
import argparse
import time

import numpy as np

from src.pdf_parser import extract_text_from_pdf
from src.rag_pipeline import chunk_text, embed_query, embed_texts, get_embedder


def cosine_sim(a: np.ndarray, b: np.ndarray):
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    sims = (a @ b) / (a_norm.flatten() * b_norm + 1e-12)
    return sims


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", help="Path to PDF file to evaluate")
    parser.add_argument(
        "--text-file", help="Path to plain text file to evaluate")
    parser.add_argument(
        "--query", default="what is the main method", help="Query for local search")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    if not args.pdf and not args.text_file:
        parser.error("Provide either --pdf or --text-file")

    if args.pdf:
        with open(args.pdf, "rb") as f:
            pdf_bytes = f.read()
        print(f"Extracting text from PDF ({args.pdf})...")
        text = extract_text_from_pdf(pdf_bytes)
    else:
        print(f"Reading text from {args.text_file}...")
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read()

    word_count = len(text.split())
    print(f"Word count: {word_count}")

    print("Chunking text...")
    chunks = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
    print(
        f"Produced {len(chunks)} chunks (chunk_size={args.chunk_size}, overlap={args.overlap})")

    embedder = get_embedder()
    start = time.time()
    vectors = embed_texts(chunks, embedder)
    embed_time = time.time() - start

    vecs = np.array(vectors)
    print(f"Embeddings shape: {vecs.shape} — computed in {embed_time:.2f}s")

    # Query embedding + local search
    qvec = np.array(embed_query(args.query, embedder))
    sims = cosine_sim(vecs, qvec)
    top_idx = np.argsort(-sims)[: args.top_k]

    print(f"\nTop {args.top_k} chunks for query: \"{args.query}\"\n")
    for rank, idx in enumerate(top_idx, start=1):
        score = float(sims[idx])
        chunk_preview = chunks[idx][:350].replace('\n', ' ')
        print(f"{rank}. chunk #{idx} — score: {score:.4f}\n   {chunk_preview}\n")

    print("Done.")


if __name__ == "__main__":
    main()

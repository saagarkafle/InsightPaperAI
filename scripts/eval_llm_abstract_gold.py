#!/usr/bin/env python3
"""
Evaluate LLM answers against paper Abstracts as proxy gold answers.

Usage:
  set -a && source .env && set +a && PYTHONPATH=. python3 scripts/eval_llm_abstract_gold.py data/eval.jsonl --top-k 5
"""
import argparse
import json
import time
from pathlib import Path
from statistics import mean

from src.llm_qa import answer_question, get_groq_client
from src.pdf_parser import extract_sections, extract_text_from_pdf
from src.rag_pipeline import chunk_text, embed_query, embed_texts, get_embedder


def normalize(text: str) -> str:
    import re
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text.lower()).split())


def f1_score(pred: str, gold: str) -> float:
    p_tokens = normalize(pred).split()
    g_tokens = normalize(gold).split()
    if not p_tokens or not g_tokens:
        return float(p_tokens == g_tokens)
    common = sum(min(p_tokens.count(t), g_tokens.count(t))
                 for t in set(p_tokens))
    if common == 0:
        return 0.0
    prec = common / len(p_tokens)
    rec = common / len(g_tokens)
    return 2 * prec * rec / (prec + rec)


def exact_match(pred: str, gold: str) -> int:
    return int(normalize(pred) == normalize(gold))


def split_sentences(text: str):
    import re
    parts = re.split(r'[\n\.!?;]+', text)
    sentences = [p.strip() for p in parts if len(p.strip()) > 20]
    return sentences


def cosine_sim(a, b):
    import numpy as np
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    sims = (a @ b) / (a_norm.flatten() * b_norm + 1e-12)
    return sims


def run_local_retrieval(chunks, query, embedder, top_k=5):
    import numpy as np

    from src.rag_pipeline import embed_query, embed_texts
    vecs = np.array(embed_texts(chunks, embedder))
    qvec = np.array(embed_query(query, embedder))
    sims = cosine_sim(vecs, qvec)
    idx_sort = list(np.argsort(-sims))
    top_idx = idx_sort[:top_k]
    return top_idx, [float(sims[i]) for i in top_idx]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('eval_file')
    p.add_argument('--top-k', type=int, default=5)
    p.add_argument('--chunk-size', type=int, default=500)
    p.add_argument('--overlap', type=int, default=100)
    args = p.parse_args()

    embedder = get_embedder()
    client = get_groq_client()

    ems = []
    f1s = []
    kp_recalls = []

    # load jsonl
    with open(args.eval_file, 'r', encoding='utf-8') as f:
        records = [json.loads(l) for l in f if l.strip()]

    for rec in records:
        qid = rec.get('id')
        query = rec.get('query')
        pdfp = rec.get('pdf')
        textf = rec.get('text_file')

        if pdfp:
            ppath = Path(pdfp)
            if not ppath.exists():
                print(f"Skipping {qid}: missing {ppath}")
                continue
            with ppath.open('rb') as fh:
                pdf_bytes = fh.read()
            text = extract_text_from_pdf(pdf_bytes)
        elif textf:
            tpath = Path(textf)
            if not tpath.exists():
                print(f"Skipping {qid}: missing {tpath}")
                continue
            text = Path(textf).read_text(encoding='utf-8')
        else:
            print(f"Skipping {qid}: no pdf/text_file")
            continue

        sections = extract_sections(text)
        gold = sections.get('Abstract') or sections.get('Abstract'.title())
        if not gold:
            gold = ' '.join(text.split()[:300])

        gold_sents = split_sentences(gold)

        chunks = chunk_text(
            text, chunk_size=args.chunk_size, overlap=args.overlap)
        if not chunks:
            continue

        top_idx, top_scores = run_local_retrieval(
            chunks, query, embedder, top_k=args.top_k)

        # build retrieved_chunks for LLM
        retrieved_chunks = []
        for rank, idx in enumerate(top_idx):
            retrieved_chunks.append({
                'text': chunks[idx],
                'score': float(top_scores[rank]) if rank < len(top_scores) else 0.0,
                'paper_title': pdfp or textf or 'unknown',
                'paper_id': qid,
                'chunk_index': int(idx),
            })

        try:
            resp = answer_question(
                query, retrieved_chunks, client=client, max_tokens=256)
            pred = resp.answer.strip()
        except Exception as e:
            print(f"LLM call failed for {qid}: {e}")
            pred = ''

        em = exact_match(pred, gold)
        f1 = f1_score(pred, gold)
        ems.append(em)
        f1s.append(f1)

        # keypoint recall: match gold sentences to retrieved chunks
        matched = 0
        for gs in gold_sents:
            best = 0.0
            for idx in top_idx:
                best = max(best, f1_score(chunks[idx], gs))
            if best >= 0.35:
                matched += 1
        kp = matched / max(1, len(gold_sents))
        kp_recalls.append(kp)

        # small sleep between requests
        time.sleep(1)

    print('\nLLM vs Abstract Results:')
    if ems:
        print(f"EM: {mean(ems):.4f}")
        print(f"F1: {mean(f1s):.4f}")
        print(f"Keypoint recall: {mean(kp_recalls):.4f}")
    else:
        print('No records evaluated')


if __name__ == '__main__':
    main()

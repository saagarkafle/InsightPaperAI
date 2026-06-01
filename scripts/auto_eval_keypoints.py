#!/usr/bin/env python3
"""
Auto-evaluate QA (extractive) and key-point recall using paper Abstracts as gold.

This is a lightweight, automatic check — it treats the paper's 'Abstract' (if found)
or the first 300 words as the gold answer. It uses the local embedder to retrieve
top-k chunks and then computes:
 - QA Exact Match and token-F1 between predicted (top-1 chunk) and gold abstract
 - Key-point recall: fraction of abstract sentences matched by any top-k chunk

Run:
  PYTHONPATH=. python3 scripts/auto_eval_keypoints.py data/eval.jsonl --top-k 5
"""
import argparse
import json
import re
from pathlib import Path
from statistics import mean

import numpy as np

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


def cosine_sim(a: np.ndarray, b: np.ndarray):
    a_norm = np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = np.linalg.norm(b)
    sims = (a @ b) / (a_norm.flatten() * b_norm + 1e-12)
    return sims


def run_local_retrieval(chunks, query, embedder, top_k=5):
    vecs = np.array(embed_texts(chunks, embedder))
    qvec = np.array(embed_query(query, embedder))
    sims = cosine_sim(vecs, qvec)
    idx_sort = list(np.argsort(-sims))
    top_idx = idx_sort[:top_k]
    top_scores = [float(sims[i]) for i in top_idx]
    return top_idx, top_scores


def split_sentences(text: str):
    parts = re.split(r'[\n\.!?;]+', text)
    sentences = [p.strip() for p in parts if len(p.strip()) > 20]
    return sentences


def load_eval(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('eval_file')
    parser.add_argument('--top-k', type=int, default=5)
    parser.add_argument('--chunk-size', type=int, default=500)
    parser.add_argument('--overlap', type=int, default=100)
    args = parser.parse_args()

    embedder = get_embedder()

    ems = []
    f1s = []
    kp_recalls = []
    details = []

    for rec in load_eval(Path(args.eval_file)):
        qid = rec.get('id')
        pdfp = rec.get('pdf')
        textf = rec.get('text_file')
        query = rec.get('query')

        if pdfp:
            p = Path(pdfp)
            if not p.exists():
                print(f"Skipping {qid}: missing {p}")
                continue
            with p.open('rb') as fh:
                pdf_bytes = fh.read()
            text = extract_text_from_pdf(pdf_bytes)
        elif textf:
            tpath = Path(textf)
            if not tpath.exists():
                print(f"Skipping {qid}: missing {tpath}")
                continue
            text = tpath.read_text(encoding='utf-8')
        else:
            print(f"Skipping {qid}: no pdf/text_file")
            continue

        sections = extract_sections(text)
        gold = sections.get('Abstract') or sections.get('Abstract'.title())
        if not gold:
            # fallback: first 300 words
            gold = ' '.join(text.split()[:300])

        # split gold into sentences (key points)
        gold_sents = split_sentences(gold)

        chunks = chunk_text(
            text, chunk_size=args.chunk_size, overlap=args.overlap)
        if not chunks:
            continue

        top_idx, top_scores = run_local_retrieval(
            chunks, query, embedder, top_k=args.top_k)

        # predicted answer = top-1 chunk
        pred = chunks[top_idx[0]] if top_idx else ''

        em = exact_match(pred, gold)
        f1 = f1_score(pred, gold)
        ems.append(em)
        f1s.append(f1)

        # key-point recall: for each gold sentence, check max F1 against any retrieved chunk
        matched = 0
        for gs in gold_sents:
            best = 0.0
            for idx in top_idx:
                best = max(best, f1_score(chunks[idx], gs))
            if best >= 0.35:
                matched += 1
        kp_recall = matched / max(1, len(gold_sents))
        kp_recalls.append(kp_recall)

        details.append({
            'id': qid,
            'pred_preview': pred[:300].replace('\n', ' '),
            'gold_preview': gold[:300].replace('\n', ' '),
            'em': em,
            'f1': f1,
            'kp_recall': kp_recall,
        })

    print('\nAuto Evaluation Results:')
    if ems:
        print(f"QA Exact Match (top-1 vs abstract): {mean(ems):.4f}")
        print(f"QA F1 (top-1 vs abstract): {mean(f1s):.4f}")
        print(f"Key-point recall (avg over queries): {mean(kp_recalls):.4f}")
    else:
        print('No records evaluated.')

    print('\nPer-query details:')
    for d in details:
        print(
            f"- {d['id']}: EM={d['em']} F1={d['f1']:.3f} KP_recall={d['kp_recall']:.3f}")


if __name__ == '__main__':
    main()

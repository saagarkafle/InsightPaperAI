#!/usr/bin/env python3
"""
Interactive annotator for eval set.

Loads `data/eval_candidates.jsonl`, shows top-K chunk previews per query,
prompts the user to mark relevant chunk indices and enter gold answers,
and writes an updated `data/eval.jsonl` (original is backed up to `.bak`).

Usage:
  PYTHONPATH=. python3 scripts/annotate_eval.py

Controls:
 - For relevant chunks enter comma-separated chunk_index values (e.g. `12,15`),
   or leave blank if none.
 - For gold answers enter one or more answers separated by `||` (e.g. `Ans1 || Ans2`),
   or leave blank to skip.
 - Enter `q` at any prompt to quit and save progress so far.
"""
import json
import shutil
from pathlib import Path


def load_jsonl(path: Path):
    items = {}
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            items[obj.get("id")] = obj
    return items


def main():
    base = Path("data")
    cand_path = base / "eval_candidates.jsonl"
    eval_path = base / "eval.jsonl"

    if not cand_path.exists():
        print(f"Candidates file not found: {cand_path}")
        return

    candidates = []
    with cand_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))

    eval_items = load_jsonl(eval_path)

    updated = {}
    for c in candidates:
        qid = c.get("id")
        query = c.get("query")
        top_k = c.get("top_k", [])

        print("\n" + "=" * 60)
        print(f"Query ID: {qid}")
        print(f"Query: {query}\n")
        print("Top candidates:")
        for t in top_k:
            print(
                f" - chunk_index={t['chunk_index']}  score={t['score']:.4f}\n   {t['preview']}\n")

        # Show existing annotations if any
        existing = eval_items.get(qid, {})
        ex_chunks = existing.get("relevant_chunk_indices", [])
        ex_golds = existing.get("gold_answers", [])
        if ex_chunks:
            print(f"Existing relevant_chunk_indices: {ex_chunks}")
        if ex_golds:
            print(f"Existing gold_answers: {ex_golds}")

        # Prompt for relevant chunks
        resp = input(
            "Enter relevant chunk_index values (comma-separated), or leave blank to keep/skip (q to quit): ").strip()
        if resp.lower() == "q":
            break
        if resp == "":
            new_chunks = ex_chunks
        else:
            parts = [p.strip() for p in resp.split(",") if p.strip()]
            try:
                new_chunks = [int(p) for p in parts]
            except ValueError:
                print("Invalid chunk indices — keeping existing.")
                new_chunks = ex_chunks

        # Prompt for gold answers
        resp2 = input(
            "Enter gold answers (separate multiple with '||'), or leave blank to keep/skip (q to quit): ").strip()
        if resp2.lower() == "q":
            break
        if resp2 == "":
            new_golds = ex_golds
        else:
            new_golds = [g.strip() for g in resp2.split("||") if g.strip()]

        # Build updated record (merge with existing fields from eval_items if present)
        base_rec = existing.copy() if existing else {
            "id": qid, "pdf": None, "text_file": None, "query": query}
        base_rec["query"] = query
        if new_chunks:
            base_rec["relevant_chunk_indices"] = new_chunks
        else:
            base_rec.pop("relevant_chunk_indices", None)
        if new_golds:
            base_rec["gold_answers"] = new_golds
        else:
            base_rec.pop("gold_answers", None)

        updated[qid] = base_rec

    # Merge updated entries into eval_items
    for k, v in updated.items():
        eval_items[k] = v

    # Backup original eval file
    if eval_path.exists():
        bak = eval_path.with_suffix(eval_path.suffix + ".bak")
        shutil.copy2(eval_path, bak)
        print(f"Backed up original {eval_path} -> {bak}")

    # Write merged eval.jsonl
    with eval_path.open("w", encoding="utf-8") as fo:
        for rec in eval_items.values():
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote updated eval set to {eval_path} ({len(eval_items)} records)")


if __name__ == "__main__":
    main()

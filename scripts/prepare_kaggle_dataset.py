#!/usr/bin/env python3
"""
scripts/prepare_kaggle_dataset.py

Download and prepare the Kaggle dataset 'tyagi586/summarized-research-papers'
for embedding model fine-tuning and RAG pipeline evaluation.

The dataset contains 150 research paper records with columns:
  Title, Authors, Publication Year, Abstract, AI-Generated Summary,
  Keywords, Field, Source Link

Outputs:
  - data/kaggle_train.jsonl  (80% — training pairs for fine-tuning)
  - data/kaggle_eval.jsonl   (20% — held-out test set for evaluation)

Usage:
  python scripts/prepare_kaggle_dataset.py
  python scripts/prepare_kaggle_dataset.py --test-ratio 0.3
"""
import argparse
import json
import logging
import os

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
TRAIN_PATH = os.path.join(DATA_DIR, "kaggle_train.jsonl")
EVAL_PATH = os.path.join(DATA_DIR, "kaggle_eval.jsonl")

KAGGLE_DATASET_ID = "tyagi586/summarized-research-papers"
KAGGLE_CSV_NAME = "summarized_research_papers.csv"


def _download_or_locate_csv() -> str:
    """Download the Kaggle CSV via kagglehub, or fall back to local cache."""
    try:
        import kagglehub
        log.info(f"Downloading dataset '{KAGGLE_DATASET_ID}' via kagglehub...")
        ds_path = kagglehub.dataset_download(KAGGLE_DATASET_ID)
        csv_file = os.path.join(ds_path, KAGGLE_CSV_NAME)
        if os.path.exists(csv_file):
            return csv_file
    except Exception as e:
        log.warning(f"Kagglehub download failed: {e}")

    # Fallback: check local cache
    fallback = os.path.expanduser(
        f"~/.cache/kagglehub/datasets/{KAGGLE_DATASET_ID}/versions/1/{KAGGLE_CSV_NAME}"
    )
    if os.path.exists(fallback):
        log.info(f"Using local cached CSV: {fallback}")
        return fallback

    raise FileNotFoundError(
        f"Could not locate {KAGGLE_CSV_NAME}. "
        "Ensure internet access or that the dataset is cached locally."
    )


def _safe_str(value) -> str:
    """Convert a DataFrame cell to a stripped string, handling NaN."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def _extract_fields(row: pd.Series) -> dict:
    """Extract and clean the standard fields from a dataset row."""
    return {
        "title": _safe_str(row.get("Title")),
        "abstract": _safe_str(row.get("Abstract")),
        "summary": _safe_str(row.get("AI-Generated Summary")),
        "keywords": _safe_str(row.get("Keywords")),
        "field": _safe_str(row.get("Field")),
    }


def _build_context(fields: dict, include_summary: bool = True) -> str:
    """Build a structured context string from extracted fields."""
    parts = []
    if fields["title"]:
        parts.append(f"Title: {fields['title']}")
    if fields["field"]:
        parts.append(f"Field: {fields['field']}")
    if fields["keywords"]:
        parts.append(f"Keywords: {fields['keywords']}")
    if fields["abstract"]:
        parts.append(f"Abstract: {fields['abstract']}")
    if include_summary and fields["summary"]:
        parts.append(f"Summary: {fields['summary']}")
    return "\n".join(parts)


def _write_jsonl(path: str, records: list[dict]) -> int:
    """Write a list of dicts as JSONL. Returns number of records written."""
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(records)


def prepare_datasets(test_ratio: float = 0.2, random_state: int = 42):
    """Download the Kaggle dataset and split into train/eval JSONL files."""
    csv_file = _download_or_locate_csv()
    df = pd.read_csv(csv_file)
    log.info(f"Loaded {len(df)} total rows from {os.path.basename(csv_file)}")

    # Deterministic shuffle and split
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    split_idx = int(len(df) * (1.0 - test_ratio))
    df_train = df.iloc[:split_idx]
    df_eval = df.iloc[split_idx:]

    os.makedirs(DATA_DIR, exist_ok=True)

    # ── Build training records ───────────────────────────────────────────────
    train_records = []
    for seq, (_, row) in enumerate(df_train.iterrows()):
        fields = _extract_fields(row)
        query = f"Research methods and key findings on {fields['title']}"
        if fields["keywords"]:
            query += f" focusing on {fields['keywords']}"

        train_records.append({
            "id": f"train_{seq}",
            "question": query,
            "context": _build_context(fields, include_summary=True),
            "answer": fields["summary"] or fields["abstract"],
            "title": fields["title"],
            "keywords": fields["keywords"],
            "field": fields["field"],
        })

    # ── Build evaluation records ─────────────────────────────────────────────
    eval_records = []
    for seq, (_, row) in enumerate(df_eval.iterrows()):
        fields = _extract_fields(row)
        query = f"What are the main findings and methodology of paper '{fields['title']}'?"

        eval_records.append({
            "id": f"eval_{seq}",
            "query": query,
            "context": _build_context(fields, include_summary=False),
            "relevant_chunk_indices": [0],
            "gold_answers": [fields["summary"] or fields["abstract"]],
            "title": fields["title"],
        })

    # ── Write output files ───────────────────────────────────────────────────
    n_train = _write_jsonl(TRAIN_PATH, train_records)
    n_eval = _write_jsonl(EVAL_PATH, eval_records)

    log.info(f"Train split: {TRAIN_PATH} ({n_train} records)")
    log.info(f"Eval split:  {EVAL_PATH} ({n_eval} records)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare Kaggle research papers dataset for training and evaluation"
    )
    parser.add_argument(
        "--test-ratio", type=float, default=0.2,
        help="Fraction of data reserved for evaluation (default: 0.2)",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for deterministic splitting (default: 42)",
    )
    args = parser.parse_args()
    prepare_datasets(test_ratio=args.test_ratio, random_state=args.seed)

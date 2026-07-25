#!/usr/bin/env python3
"""
scripts/prepare_kaggle_dataset.py

Download and prepare the Kaggle dataset 'tyagi586/summarized-research-papers'
for embedding model fine-tuning and RAG pipeline evaluation.

Outputs:
  - data/kaggle_train.jsonl (120 samples for training)
  - data/kaggle_eval.jsonl  (30 samples for evaluation)
"""
import json
import logging
import os
import sys
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


def download_or_get_path():
    try:
        import kagglehub
        log.info("Downloading dataset 'tyagi586/summarized-research-papers' via kagglehub...")
        ds_path = kagglehub.dataset_download("tyagi586/summarized-research-papers")
        csv_file = os.path.join(ds_path, "summarized_research_papers.csv")
        if os.path.exists(csv_file):
            return csv_file
    except Exception as e:
        log.warning(f"Kagglehub download attempt failed: {e}")

    # Fallback to local cache path if existing
    fallback = os.path.expanduser("~/.cache/kagglehub/datasets/tyagi586/summarized-research-papers/versions/1/summarized_research_papers.csv")
    if os.path.exists(fallback):
        log.info(f"Using local cached CSV: {fallback}")
        return fallback

    raise FileNotFoundError("Could not locate summarized_research_papers.csv. Please ensure internet access or provide local file.")


def prepare_datasets(test_ratio=0.2, random_state=42):
    csv_file = download_or_get_path()
    df = pd.read_csv(csv_file)
    log.info(f"Loaded {len(df)} total rows from {os.path.basename(csv_file)}")

    # Shuffle deterministically
    df_shuffled = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)

    split_idx = int(len(df_shuffled) * (1.0 - test_ratio))
    df_train = df_shuffled.iloc[:split_idx]
    df_eval = df_shuffled.iloc[split_idx:]

    os.makedirs(DATA_DIR, exist_ok=True)

    # Prepare Train split
    train_count = 0
    with open(TRAIN_PATH, "w", encoding="utf-8") as f:
        for idx, row in df_train.iterrows():
            title = str(row.get("Title", "")).strip()
            abstract = str(row.get("Abstract", "")).strip()
            summary = str(row.get("AI-Generated Summary", "")).strip()
            keywords = str(row.get("Keywords", "")).strip()
            field = str(row.get("Field", "")).strip()

            query = f"Research methods and key findings on {title}"
            if keywords:
                query += f" focusing on {keywords}"

            context = f"Title: {title}\nField: {field}\nKeywords: {keywords}\nAbstract: {abstract}\nSummary: {summary}"

            item = {
                "id": f"train_{idx}",
                "question": query,
                "context": context,
                "answer": summary if summary else abstract,
                "title": title,
                "keywords": keywords,
                "field": field
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            train_count += 1

    # Prepare Eval split
    eval_count = 0
    with open(EVAL_PATH, "w", encoding="utf-8") as f:
        for idx, row in df_eval.iterrows():
            title = str(row.get("Title", "")).strip()
            abstract = str(row.get("Abstract", "")).strip()
            summary = str(row.get("AI-Generated Summary", "")).strip()
            keywords = str(row.get("Keywords", "")).strip()
            field = str(row.get("Field", "")).strip()

            query = f"What are the main findings and methodology of paper '{title}'?"
            context = f"Title: {title}\nField: {field}\nKeywords: {keywords}\nAbstract: {abstract}"

            item = {
                "id": f"eval_{idx}",
                "query": query,
                "context": context,
                "relevant_chunk_indices": [0],
                "gold_answers": [summary] if summary else [abstract],
                "title": title
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            eval_count += 1

    log.info(f"Successfully generated train split: {TRAIN_PATH} ({train_count} records)")
    log.info(f"Successfully generated eval split:  {EVAL_PATH} ({eval_count} records)")


if __name__ == "__main__":
    prepare_datasets()

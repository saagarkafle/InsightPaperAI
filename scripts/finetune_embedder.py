"""
scripts/finetune_embedder.py

Fine-tune the all-MiniLM-L6-v2 embedding model on SQuAD v2.

What this does:
  - Downloads SQuAD v2 from Hugging Face (~87k answerable Q&A pairs)
  - Trains the embedding model on (question, context) pairs
  - The model learns: "questions should be close to their relevant context in vector space"
  - Saves the fine-tuned model to: models/fine_tuned_embedder/
  - Next time you run the app, it automatically uses the fine-tuned model

Run with:
  source venv/bin/activate
  python scripts/finetune_embedder.py

Expected time:
  ~10-15 minutes on CPU, ~3-5 minutes on GPU
"""

import logging
import os
import sys

# ─── Config ───────────────────────────────────────────────────────────────────
BASE_MODEL = "all-MiniLM-L6-v2"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "models", "fine_tuned_embedder")
MAX_SAMPLES = 30_000    # 30k pairs — enough to improve, fast enough to run
BATCH_SIZE = 32
EPOCHS = 1
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def check_dependencies():
    """Make sure required libraries are installed."""
    missing = []
    try:
        import datasets
    except ImportError:
        missing.append("datasets")
    try:
        import sentence_transformers
    except ImportError:
        missing.append("sentence-transformers")
    try:
        import torch
    except ImportError:
        missing.append("torch")

    if missing:
        log.error(f"Missing packages: {', '.join(missing)}")
        log.error(f"Install with:  pip install {' '.join(missing)}")
        sys.exit(1)


def load_squad_pairs(max_samples: int):
    """
    Load SQuAD v2 training split and extract (question, context) pairs.
    Skips unanswerable questions (SQuAD v2 has ~43k of these).
    Returns a list of sentence_transformers InputExample objects.
    """
    from datasets import load_dataset
    from sentence_transformers import InputExample

    log.info("Downloading rajpurkar/squad_v2 from Hugging Face...")
    log.info("(This may take a minute on first download — cached afterwards)")
    ds = load_dataset("rajpurkar/squad_v2", split="train")

    examples = []
    skipped = 0

    for row in ds:
        # Skip unanswerable questions — no context to learn from
        if not row["answers"]["text"]:
            skipped += 1
            continue

        question = row["question"].strip()
        context = row["context"].strip()

        if question and context:
            examples.append(InputExample(texts=[question, context]))

        if len(examples) >= max_samples:
            break

    log.info(f"Loaded   {len(examples):>6,} training pairs")
    log.info(f"Skipped  {skipped:>6,} unanswerable questions")
    return examples


def load_jsonl_pairs(filepath: str, max_samples: int):
    """
    Load training pairs from a JSONL file (e.g. data/kaggle_train.jsonl).
    Extracts (question/query/title, context/abstract/answer) pairs.
    """
    import json
    from sentence_transformers import InputExample

    log.info(f"Loading training pairs from JSONL: {filepath}")
    examples = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            question = item.get("question") or item.get("query") or item.get("title", "")
            context = item.get("context") or item.get("abstract") or item.get("answer", "")
            if question and context:
                examples.append(InputExample(texts=[str(question).strip(), str(context).strip()]))
            if len(examples) >= max_samples:
                break

    log.info(f"Loaded   {len(examples):>6,} training pairs from {os.path.basename(filepath)}")
    return examples


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fine-tune embedding model on research Q&A pairs")
    parser.add_argument("--dataset", default=None, help="Path to JSONL dataset file (e.g. data/kaggle_train.jsonl)")
    parser.add_argument("--use-kaggle", action="store_true", help="Use pre-generated data/kaggle_train.jsonl dataset")
    parser.add_argument("--base-model", default=BASE_MODEL, help="Base Hugging Face model or path")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="Directory to save fine-tuned model")
    parser.add_argument("--epochs", type=int, default=EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size for training")
    parser.add_argument("--max-samples", type=int, default=MAX_SAMPLES, help="Max dataset samples")
    args = parser.parse_args()

    check_dependencies()

    from sentence_transformers import SentenceTransformer, losses
    from torch.utils.data import DataLoader

    output_dir = args.output_dir

    # ── Load base model ──────────────────────────────────────────────────────
    log.info(f"Loading base model: {args.base_model}")
    model = SentenceTransformer(args.base_model)

    # ── Load training data ───────────────────────────────────────────────────
    dataset_path = args.dataset
    if args.use_kaggle or (not dataset_path and os.path.exists(os.path.join(PROJECT_ROOT, "data", "kaggle_train.jsonl"))):
        dataset_path = os.path.join(PROJECT_ROOT, "data", "kaggle_train.jsonl")

    if dataset_path and os.path.exists(dataset_path):
        train_examples = load_jsonl_pairs(dataset_path, args.max_samples)
    else:
        log.info("No local JSONL specified/found. Falling back to Hugging Face SQuAD v2...")
        train_examples = load_squad_pairs(args.max_samples)

    if not train_examples:
        log.error("No training pairs loaded! Exiting.")
        sys.exit(1)

    train_dataloader = DataLoader(
        train_examples,
        shuffle=True,
        batch_size=args.batch_size,
    )

    # ── Loss: Multiple Negatives Ranking Loss ────────────────────────────────
    train_loss = losses.MultipleNegativesRankingLoss(model)

    warmup_steps = int(len(train_dataloader) * args.epochs * 0.1)

    log.info(f"Starting fine-tuning...")
    log.info(f"  Pairs:       {len(train_examples):,}")
    log.info(f"  Batch size:  {args.batch_size}")
    log.info(f"  Epochs:      {args.epochs}")
    log.info(f"  Warmup:      {warmup_steps} steps")
    log.info(f"  Output:      {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # ── Train ────────────────────────────────────────────────────────────────
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=args.epochs,
        warmup_steps=warmup_steps,
        output_path=output_dir,
        show_progress_bar=True,
        checkpoint_save_steps=5000,
        checkpoint_path=output_dir,
    )

    log.info("=" * 60)
    log.info("Fine-tuning complete!")
    log.info(f"Model saved to: {output_dir}")
    log.info("Restart the Streamlit app to use the fine-tuned model.")
    log.info("=" * 60)


if __name__ == "__main__":
    main()

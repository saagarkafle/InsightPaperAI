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


def main():
    check_dependencies()

    from sentence_transformers import SentenceTransformer, losses
    from torch.utils.data import DataLoader

    # ── Load base model ──────────────────────────────────────────────────────
    log.info(f"Loading base model: {BASE_MODEL}")
    model = SentenceTransformer(BASE_MODEL)

    # ── Load training data ───────────────────────────────────────────────────
    train_examples = load_squad_pairs(MAX_SAMPLES)

    train_dataloader = DataLoader(
        train_examples,
        shuffle=True,
        batch_size=BATCH_SIZE,
    )

    # ── Loss: Multiple Negatives Ranking Loss ────────────────────────────────
    # For each (question, context) pair in a batch, all other contexts in that
    # batch act as negatives. The model learns to pull matching pairs together
    # and push non-matching pairs apart. No explicit negative labels needed.
    train_loss = losses.MultipleNegativesRankingLoss(model)

    warmup_steps = int(len(train_dataloader) * EPOCHS * 0.1)

    log.info(f"Starting fine-tuning...")
    log.info(f"  Pairs:       {len(train_examples):,}")
    log.info(f"  Batch size:  {BATCH_SIZE}")
    log.info(f"  Epochs:      {EPOCHS}")
    log.info(f"  Warmup:      {warmup_steps} steps")
    log.info(f"  Output:      {OUTPUT_DIR}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Train ────────────────────────────────────────────────────────────────
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=EPOCHS,
        warmup_steps=warmup_steps,
        output_path=OUTPUT_DIR,
        show_progress_bar=True,
        checkpoint_save_steps=5000,
        checkpoint_path=OUTPUT_DIR,
    )

    log.info("=" * 60)
    log.info("Fine-tuning complete!")
    log.info(f"Model saved to: {OUTPUT_DIR}")
    log.info("Restart the Streamlit app to use the fine-tuned model.")
    log.info("=" * 60)


if __name__ == "__main__":
    main()

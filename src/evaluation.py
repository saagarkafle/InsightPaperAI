# src/evaluation.py — Automatic Evaluation using Dataset Gold Answers
import re

import numpy as np


def _tokenize(text: str) -> set[str]:
    """Simple whitespace + punctuation tokenizer for overlap scoring."""
    return set(re.sub(r"[^\w\s]", "", text.lower()).split())


def exact_match_f1(predicted: str, gold: str) -> float:
    """
    Token-overlap F1 score between predicted and gold answers.
    Returns a float in [0, 1].
    """
    pred_tokens = _tokenize(predicted)
    gold_tokens = _tokenize(gold)

    if not pred_tokens or not gold_tokens:
        return 0.0

    common = pred_tokens & gold_tokens
    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gold_tokens)
    f1 = 2 * precision * recall / (precision + recall)
    return round(f1, 4)


def semantic_similarity_score(predicted: str, gold: str, embedder) -> float:
    """
    Cosine similarity between sentence embeddings of predicted and gold.
    Uses the same embedder already loaded (all-MiniLM-L6-v2).
    """
    if not predicted.strip() or not gold.strip():
        return 0.0

    vectors = embedder.encode([predicted, gold], show_progress_bar=False)
    pred_vec = vectors[0]
    gold_vec = vectors[1]

    dot = np.dot(pred_vec, gold_vec)
    norm_pred = np.linalg.norm(pred_vec)
    norm_gold = np.linalg.norm(gold_vec)

    if norm_pred == 0 or norm_gold == 0:
        return 0.0

    similarity = dot / (norm_pred * norm_gold)
    return round(float(similarity), 4)


def evaluate_single(
    question: str,
    gold_answer: str,
    model_answer: str,
    embedder,
) -> dict:
    """Evaluate a single question-answer pair."""
    return {
        "question": question,
        "gold_answer": gold_answer,
        "model_answer": model_answer,
        "f1_score": exact_match_f1(model_answer, gold_answer),
        "semantic_similarity": semantic_similarity_score(model_answer, gold_answer, embedder),
    }


def compute_aggregate_metrics(results: list[dict]) -> dict:
    """Compute aggregate metrics from a list of evaluation results."""
    if not results:
        return {"mean_f1": 0.0, "mean_semantic": 0.0, "count": 0}

    f1_scores = [r["f1_score"] for r in results]
    sem_scores = [r["semantic_similarity"] for r in results]

    return {
        "mean_f1": round(sum(f1_scores) / len(f1_scores), 4),
        "mean_semantic": round(sum(sem_scores) / len(sem_scores), 4),
        "count": len(results),
    }

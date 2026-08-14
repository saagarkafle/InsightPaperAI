# src/evaluation.py — Automatic Evaluation using Dataset Gold Answers & LLM-as-a-Judge
import json
import re

import numpy as np

from src.llm_utils import parse_json_response


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


def evaluate_llm_as_judge(
    question: str,
    gold_answer: str,
    model_answer: str,
    context: str,
    client,
    judge_model: str = "llama-3.1-8b-instant",
) -> dict:
    """
    LLM-as-a-Judge evaluation paradigm (Zheng et al., 2023).
    Evaluates model_answer against context & gold_answer on 1-5 scales:
      - Faithfulness (0 hallucination)
      - Answer Relevance (directness)
      - Completeness
    Returns a dict with scores and reasoning.
    """
    if not client:
        return {
            "faithfulness": 0,
            "relevance": 0,
            "completeness": 0,
            "overall_score": 0.0,
            "reasoning": "No Groq client provided",
        }

    prompt = f"""You are an expert impartial AI research judge evaluating a Retrieval-Augmented Generation (RAG) system.

QUESTION: {question}

RETRIEVED CONTEXT:
{context[:2000]}

GENERATED MODEL ANSWER:
{model_answer}

REFERENCE GOLD ANSWER:
{gold_answer}

Rate the GENERATED MODEL ANSWER on integer scales from 1 to 5:
1. "faithfulness": (1-5) Is the model answer fully grounded in the retrieved context without making up unverified facts? (5 = perfect zero-hallucination)
2. "relevance": (1-5) Does it directly address the user's question? (5 = completely relevant)
3. "completeness": (1-5) Does it capture key facts from the reference gold answer and context clearly? (5 = comprehensive and clear)

Return ONLY a valid JSON object with these keys:
{{
  "faithfulness": 5,
  "relevance": 5,
  "completeness": 5,
  "overall_score": 5.0,
  "reasoning": "brief 1-sentence explanation"
}}
"""

    try:
        response = client.chat.completions.create(
            model=judge_model,
            messages=[
                {"role": "system", "content": "You are an expert AI evaluator. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=300,
        )
        data = parse_json_response(response.choices[0].message.content)
        return {
            "faithfulness": int(data.get("faithfulness", 3)),
            "relevance": int(data.get("relevance", 3)),
            "completeness": int(data.get("completeness", 3)),
            "overall_score": float(data.get("overall_score", 3.0)),
            "reasoning": str(data.get("reasoning", "Evaluated by LLM Judge.")),
        }
    except Exception as e:
        return {
            "faithfulness": 0,
            "relevance": 0,
            "completeness": 0,
            "overall_score": 0.0,
            "reasoning": f"Judge evaluation error: {e}",
        }


def evaluate_single(
    question: str,
    gold_answer: str,
    model_answer: str,
    embedder,
    context: str = "",
    client=None,
    judge_model: str = "llama-3.1-8b-instant",
) -> dict:
    """Evaluate a single question-answer pair with traditional metrics + optional LLM-as-a-Judge."""
    res = {
        "question": question,
        "gold_answer": gold_answer,
        "model_answer": model_answer,
        "f1_score": exact_match_f1(model_answer, gold_answer),
        "semantic_similarity": semantic_similarity_score(model_answer, gold_answer, embedder),
    }
    if client and context:
        judge_res = evaluate_llm_as_judge(
            question=question,
            gold_answer=gold_answer,
            model_answer=model_answer,
            context=context,
            client=client,
            judge_model=judge_model,
        )
        res["llm_judge"] = judge_res
    return res


def compute_aggregate_metrics(results: list[dict]) -> dict:
    """Compute aggregate metrics from a list of evaluation results."""
    if not results:
        return {"mean_f1": 0.0, "mean_semantic": 0.0, "count": 0}

    f1_scores = [r["f1_score"] for r in results]
    sem_scores = [r["semantic_similarity"] for r in results]

    agg = {
        "mean_f1": round(sum(f1_scores) / len(f1_scores), 4),
        "mean_semantic": round(sum(sem_scores) / len(sem_scores), 4),
        "count": len(results),
    }

    judge_scores = [r["llm_judge"]["overall_score"] for r in results if "llm_judge" in r]
    faithfulness_scores = [r["llm_judge"]["faithfulness"] for r in results if "llm_judge" in r]
    relevance_scores = [r["llm_judge"]["relevance"] for r in results if "llm_judge" in r]
    completeness_scores = [r["llm_judge"]["completeness"] for r in results if "llm_judge" in r]

    if judge_scores:
        agg["mean_judge_overall"] = round(sum(judge_scores) / len(judge_scores), 2)
        agg["mean_faithfulness"] = round(sum(faithfulness_scores) / len(faithfulness_scores), 2)
        agg["mean_relevance"] = round(sum(relevance_scores) / len(relevance_scores), 2)
        agg["mean_completeness"] = round(sum(completeness_scores) / len(completeness_scores), 2)

    return agg

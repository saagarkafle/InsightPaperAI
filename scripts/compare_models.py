"""
scripts/compare_models.py

Compares the base all-MiniLM-L6-v2 model against the fine-tuned version
on a set of question-context pairs.

Shows: how much more similar the fine-tuned model considers
a question to its correct answer context vs a wrong context.

Run with:
  source venv/bin/activate
  python3 scripts/compare_models.py
"""

import os
import sys
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINE_TUNED_PATH = os.path.join(PROJECT_ROOT, "models", "fine_tuned_embedder")

# ── Sample Q&A pairs (question + correct context + a wrong/unrelated context)
SAMPLES = [
    {
        "question": "What is the main method used in the study?",
        "correct_context": "The study proposes a transformer-based architecture "
                           "that uses self-attention mechanisms to encode contextual "
                           "information across the entire input sequence simultaneously.",
        "wrong_context":  "The experiment was conducted in a laboratory setting with "
                          "a sample size of 42 participants aged between 18 and 35 years.",
    },
    {
        "question": "What datasets were used for evaluation?",
        "correct_context": "The model was evaluated on three benchmark datasets: "
                           "SQuAD 1.1, TriviaQA, and Natural Questions, achieving "
                           "state-of-the-art results on all three.",
        "wrong_context":  "The city has a population of approximately 2.3 million "
                          "people and covers an area of 1,572 square kilometres.",
    },
    {
        "question": "What are the limitations of this approach?",
        "correct_context": "Despite strong performance, the method has notable limitations. "
                           "It requires large amounts of labelled training data and "
                           "struggles to generalise to low-resource languages.",
        "wrong_context":  "Photosynthesis is the process by which plants use sunlight, "
                          "water and carbon dioxide to produce oxygen and energy.",
    },
    {
        "question": "What is the proposed solution to the problem?",
        "correct_context": "We introduce a novel retrieval-augmented generation pipeline "
                           "that first retrieves relevant passages from a document store "
                           "and then conditions the language model on those passages.",
        "wrong_context":  "The stock market closed higher on Friday, with the S&P 500 "
                          "gaining 1.2 percent driven by technology sector gains.",
    },
]


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def score_model(model, samples):
    results = []
    for s in samples:
        vecs = model.encode(
            [s["question"], s["correct_context"], s["wrong_context"]],
            show_progress_bar=False,
        )
        correct_sim = cosine_similarity(vecs[0], vecs[1])
        wrong_sim   = cosine_similarity(vecs[0], vecs[2])
        margin      = correct_sim - wrong_sim
        results.append({
            "question":    s["question"],
            "correct_sim": round(correct_sim, 4),
            "wrong_sim":   round(wrong_sim, 4),
            "margin":      round(margin, 4),
        })
    return results


def main():
    from sentence_transformers import SentenceTransformer

    if not os.path.isdir(FINE_TUNED_PATH):
        print("ERROR: Fine-tuned model not found at:", FINE_TUNED_PATH)
        print("Run scripts/finetune_embedder.py first.")
        sys.exit(1)

    print("Loading models...")
    base_model      = SentenceTransformer("all-MiniLM-L6-v2")
    finetuned_model = SentenceTransformer(FINE_TUNED_PATH)
    print("Done.\n")

    base_results      = score_model(base_model, SAMPLES)
    finetuned_results = score_model(finetuned_model, SAMPLES)

    # ── Print comparison table ────────────────────────────────────────────────
    col = 42
    print("=" * 90)
    print(f"  {'QUESTION':<{col}}  {'CORRECT SIM':>11}  {'WRONG SIM':>9}  {'MARGIN':>7}")
    print("=" * 90)

    for label, results in [("BASE MODEL", base_results), ("FINE-TUNED MODEL", finetuned_results)]:
        print(f"\n  [{label}]")
        for r in results:
            q = r["question"][:col]
            print(f"  {q:<{col}}  {r['correct_sim']:>11.4f}  {r['wrong_sim']:>9.4f}  {r['margin']:>+7.4f}")

    # ── Averages ──────────────────────────────────────────────────────────────
    avg_base_margin = sum(r["margin"] for r in base_results) / len(base_results)
    avg_ft_margin   = sum(r["margin"] for r in finetuned_results) / len(finetuned_results)
    improvement     = ((avg_ft_margin - avg_base_margin) / abs(avg_base_margin)) * 100

    print("\n" + "=" * 90)
    print(f"  Average margin (correct - wrong similarity)")
    print(f"    Base model:       {avg_base_margin:+.4f}")
    print(f"    Fine-tuned model: {avg_ft_margin:+.4f}")
    print(f"    Improvement:      {improvement:+.1f}%")
    print("=" * 90)

    # ── Explanation ───────────────────────────────────────────────────────────
    print("""
WHAT THIS MEANS:
  'Correct sim'  = cosine similarity between the question and the RIGHT answer context.
  'Wrong sim'    = cosine similarity between the question and an UNRELATED context.
  'Margin'       = correct_sim - wrong_sim (higher = better at separating relevant from noise).

  A larger margin means the model is better at ranking the correct passage above
  irrelevant ones — which is exactly what happens during semantic search in the app.
""")


if __name__ == "__main__":
    main()

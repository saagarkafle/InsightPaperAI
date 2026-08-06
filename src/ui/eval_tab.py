# src/ui/eval_tab.py — Evaluation tab rendering (extracted from tabs.py)
import html as html_mod

import streamlit as st

from src.llm_qa import resolve_model_id
from src.stream_helpers import get_source_filter


def run_evaluation(eval_rows: list[dict]) -> None:
    """Run the evaluation pipeline on selected rows."""
    from src.evaluation import compute_aggregate_metrics, evaluate_single
    from src.llm_qa import answer_question
    from src.rag_pipeline import semantic_search

    model_id = resolve_model_id(st.session_state.get("selected_model"))

    results = []
    progress_bar = st.progress(0.0)
    status_text = st.empty()

    source_mode = st.session_state.get("source_mode", "both")
    has_pdf = bool(st.session_state.papers)
    has_dataset = bool(st.session_state.get("dataset"))
    sf = get_source_filter(source_mode, has_pdf, has_dataset)

    for i, row in enumerate(eval_rows):
        question = row["question"]
        gold_answer = row["answer"]

        status_text.text(f"Evaluating question {i+1}/{len(eval_rows)}...")
        progress_bar.progress((i + 1) / len(eval_rows))

        # Retrieve and generate answer
        chunks = semantic_search(
            query=question,
            embedder=st.session_state.embedder,
            index=st.session_state.index,
            top_k=5,
            filter_paper_id=st.session_state.active_paper_id if sf != "dataset" else None,
            source_filter=sf,
        )

        response = answer_question(
            question=question,
            retrieved_chunks=chunks,
            client=st.session_state.groq_client,
            model=model_id,
        )

        # Build context string for LLM Judge
        context_text = "\n\n".join([c.get("text", "") for c in chunks])

        result = evaluate_single(
            question=question,
            gold_answer=gold_answer,
            model_answer=response.answer,
            embedder=st.session_state.embedder,
            context=context_text,
            client=st.session_state.groq_client,
        )
        results.append(result)

    progress_bar.empty()
    status_text.empty()

    # Store results
    st.session_state.eval_results = {
        "results": results,
        "aggregate": compute_aggregate_metrics(results),
    }
    st.rerun()


def display_eval_results(eval_data: dict) -> None:
    """Display evaluation results in a clean table format."""
    results = eval_data.get("results", [])
    aggregate = eval_data.get("aggregate", {})

    if not results:
        return

    # Aggregate metrics
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        "<span class='section-label'>Aggregate Metrics</span>",
        unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Mean F1 Score", f"{aggregate.get('mean_f1', 0):.2%}")
    mc2.metric("Mean Semantic Sim", f"{aggregate.get('mean_semantic', 0):.2%}")
    if "mean_judge_overall" in aggregate:
        mc3.metric("LLM Judge Rating", f"{aggregate.get('mean_judge_overall', 0):.1f} / 5.0")
        mc4.metric("Faithfulness (0-hallucination)", f"{aggregate.get('mean_faithfulness', 0):.1f} / 5.0")
    else:
        mc3.metric("Questions Evaluated", aggregate.get("count", 0))
        mc4.metric("Evaluation Status", "Complete")

    # Per-question results
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<span class='section-label'>Per-Question Results</span>",
        unsafe_allow_html=True)

    for i, r in enumerate(results):
        f1 = r["f1_score"]
        sem = r["semantic_similarity"]

        f1_class = "eval-score-good" if f1 >= 0.5 else ("eval-score-mid" if f1 >= 0.25 else "eval-score-low")
        sem_class = "eval-score-good" if sem >= 0.7 else ("eval-score-mid" if sem >= 0.5 else "eval-score-low")

        judge_html = ""
        if "llm_judge" in r:
            j = r["llm_judge"]
            judge_html = f"""
            <div style="margin-top:6px; font-size:12px; color:var(--text-secondary);">
                <strong>🤖 LLM Judge:</strong> {j.get('overall_score', 0):.1f}/5.0
                &nbsp;|&nbsp; Faithfulness: <strong>{j.get('faithfulness', 0)}/5</strong>
                &nbsp;|&nbsp; Relevance: <strong>{j.get('relevance', 0)}/5</strong>
                &nbsp;|&nbsp; Completeness: <strong>{j.get('completeness', 0)}/5</strong><br/>
                <span style="font-style:italic; color:var(--text-muted);">{html_mod.escape(j.get('reasoning', ''))}</span>
            </div>
            """

        with st.expander(f"Q{i+1}: {r['question'][:80]}...", expanded=(i == 0)):
            st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <strong>Question:</strong> {html_mod.escape(r['question'])}
            </div>
            <div style="margin-bottom: 8px;">
                <strong>Gold Answer:</strong> <span style="color: var(--text-secondary);">{html_mod.escape(r['gold_answer'])}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <strong>Model Answer:</strong> {html_mod.escape(r['model_answer'])}
            </div>
            <div style="display: flex; gap: 16px; font-size: 13px;">
                <span>F1 Score: <span class="{f1_class}">{f1:.4f}</span></span>
                <span>Semantic Sim: <span class="{sem_class}">{sem:.4f}</span></span>
            </div>
            {judge_html}
            """, unsafe_allow_html=True)

        safe_q = html_mod.escape(r["question"][:150])
        safe_gold = html_mod.escape(r["gold_answer"][:200])
        safe_model = html_mod.escape(r["model_answer"][:200])

        st.markdown(f"""
        <div class="eval-row">
            <div class="eval-question">Q{i+1}: {safe_q}</div>
            <div style="margin-bottom:8px;">
                <span class="eval-score {f1_class}">F1: {f1:.2%}</span>
                <span class="eval-score {sem_class}">Semantic: {sem:.2%}</span>
            </div>
            <div style="font-size:12px; color:var(--muted); margin-bottom:4px;"><strong>Gold:</strong> {safe_gold}</div>
            <div style="font-size:12px; color:var(--text-secondary);"><strong>Model:</strong> {safe_model}</div>
        </div>
        """, unsafe_allow_html=True)

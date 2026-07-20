import html as html_mod

import streamlit as st

from src.rag_pipeline import semantic_search
from src.stream_helpers import render_question_turn


def populate_tabs(tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate):
    selected = st.session_state.get('selected_tab', 'Ask Questions')
    source_mode = st.session_state.get('source_mode', 'both')

    # ──────────────────────────────────────────
    # CHAT TAB
    # ──────────────────────────────────────────
    with tab_chat:
        if selected == 'Ask Questions':
            if not st.session_state.messages:
                st.markdown(
                    "<span class='section-label' style='border-bottom:none;'>Try these questions</span>",
                    unsafe_allow_html=True)
                suggestions = [
                    "What problem does this paper solve?",
                    "What is the main methodology or approach?",
                    "What are the key results and findings?",
                    "What datasets were used for evaluation?",
                    "What are the limitations of this work?",
                    "How does this compare to previous approaches?",
                ]
                cols = st.columns(2)
                for i, q in enumerate(suggestions):
                    with cols[i % 2]:
                        if st.button(q, key=f"quick_q_{i}", use_container_width=True):
                            st.session_state.quick_question = q
                st.markdown("<div style='height:16px'></div>",
                            unsafe_allow_html=True)

            # Chat history
            for msg in st.session_state.messages:
                avatar = "🧑‍💻" if msg["role"] == "user" else "📚"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant":
                        saved_figs = msg.get("matched_figures", [])
                        if saved_figs:
                            st.markdown(
                                "<div class='fig-match-banner'>📌 Related Figures</div>",
                                unsafe_allow_html=True)
                            fig_cols = st.columns(len(saved_figs))
                            for col, fig in zip(fig_cols, saved_figs):
                                with col:
                                    caption = f"{fig.fig_label}"
                                    if fig.caption:
                                        caption += f" — {fig.caption}"
                                    st.image(
                                        f"data:image/png;base64,{fig.image_base64}",
                                        caption=caption, width="stretch")
                        if "sources" in msg:
                            with st.expander(f"📎 {len(msg['sources'])} source chunks"):
                                for src in msg["sources"]:
                                    source_type = src.get("source_type", "pdf")
                                    type_badge = "📄 PDF" if source_type == "pdf" else "📊 Dataset"
                                    st.markdown(f"""
                                    <div class="source-chunk">
                                        <span class="score-badge">score: {src['score']}</span>
                                        <span class="source-type-badge">{type_badge}</span>
                                        &nbsp; chunk #{src['chunk_index']}<br/><br/>
                                        {html_mod.escape(src['text'][:300])}...
                                    </div>""", unsafe_allow_html=True)
                        if "meta" in msg:
                            m = msg["meta"]
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Latency", f"{m['latency_ms']:.0f}ms")
                            c2.metric(
                                "Tokens", f"{m['tokens_in']}→{m['tokens_out']}")
                            c3.metric("Sources", len(msg.get("sources", [])))

            quick_question = st.session_state.pop("quick_question", None)
            if quick_question:
                render_question_turn(
                    quick_question,
                    st.session_state.active_paper_id,
                    st.session_state.papers.get(
                        st.session_state.active_paper_id, {}).get("figures", []),
                    source_mode=source_mode,
                )
                st.rerun()

            if prompt := st.chat_input("Ask anything about this paper..."):
                render_question_turn(
                    prompt,
                    st.session_state.active_paper_id,
                    st.session_state.papers.get(
                        st.session_state.active_paper_id, {}).get("figures", []),
                    source_mode=source_mode,
                )

            if st.session_state.messages:
                if st.button("🗑 Clear Chat"):
                    st.session_state.messages = []
                    st.rerun()

    # ──────────────────────────────────────────
    # FIGURES TAB
    # ──────────────────────────────────────────
    with tab_figures:
        if selected.startswith('Figures'):
            paper_figures = st.session_state.papers.get(
                st.session_state.active_paper_id, {}).get("figures", [])
            if not paper_figures:
                st.markdown("""
                <div style="text-align:center; padding:48px; color:var(--muted);">
                    <div style="font-size:32px; margin-bottom:8px;">🖼</div>
                    <div style="font-size:14px; color:var(--text);">No figures found in this paper.</div>
                    <div style="font-size:12px; margin-top:6px; color:var(--soft);">Some PDFs store images in formats that cannot be extracted.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='padding:8px 0 12px 0; font-size:13px; color:var(--muted);'>{len(paper_figures)} figures extracted</div>",
                    unsafe_allow_html=True)
                for i in range(0, len(paper_figures), 2):
                    cols = st.columns(2)
                    for j, col in enumerate(cols):
                        if i + j < len(paper_figures):
                            fig = paper_figures[i + j]
                            with col:
                                with st.container():
                                    safe_label = html_mod.escape(fig.fig_label)
                                    safe_caption = html_mod.escape(
                                        fig.caption) if fig.caption else "No caption detected"
                                    st.markdown(f"""
                                    <div class="fig-card">
                                        <div class="fig-label">{safe_label} · Page {fig.page}</div>
                                        <div class="fig-caption">{safe_caption}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.image(
                                        f"data:image/png;base64,{fig.image_base64}",
                                        width="stretch")
                                    st.markdown(
                                        "<div style='height:8px'></div>",
                                        unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # SEARCH TAB
    # ──────────────────────────────────────────
    with tab_search:
        if selected == 'Search':
            st.markdown("<div style='height:8px'></div>",
                        unsafe_allow_html=True)
            st.markdown(
                "<span class='sec-label'>Search paper chunks by semantic similarity</span>",
                unsafe_allow_html=True)
            st.markdown("<div class='search-results-scroll'>",
                        unsafe_allow_html=True)
            search_col, k_col = st.columns([4, 1])
            with search_col:
                search_query = st.text_input(
                    "Search Query",
                    placeholder="e.g. attention mechanism, loss function, dataset...",
                    label_visibility="collapsed")
            with k_col:
                top_k = st.selectbox(
                    "Top K", [3, 5, 8, 10], index=1,
                    label_visibility="collapsed")
            if search_query:
                # Determine source filter for search
                sf = None
                if source_mode == "pdf":
                    sf = "pdf"
                elif source_mode == "dataset":
                    sf = "dataset"

                with st.spinner("Searching..."):
                    results = semantic_search(
                        query=search_query,
                        embedder=st.session_state.embedder,
                        index=st.session_state.index,
                        top_k=top_k,
                        filter_paper_id=st.session_state.active_paper_id if sf != "dataset" else None,
                        source_filter=sf,
                    )
                st.markdown(
                    f"<div style='font-size:12px; color:var(--muted); margin:10px 0;'>Found {len(results)} chunks</div>",
                    unsafe_allow_html=True)
                for r in results:
                    score_pct = int(r["score"] * 100)
                    source_type = r.get("source_type", "pdf")
                    type_label = "📄 PDF" if source_type == "pdf" else "📊 Dataset"
                    with st.expander(
                        f"{type_label} · Chunk #{r['chunk_index']} — Score: {r['score']} ({score_pct}% match)"
                    ):
                        st.progress(r["score"])
                        st.markdown(f"""
                        <div class="source-chunk">{html_mod.escape(r['text'])}</div>""",
                                    unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # STATS TAB
    # ──────────────────────────────────────────
    with tab_stats:
        if selected == 'Stats':
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Papers Indexed", len(st.session_state.papers))
            c2.metric("Total Chunks", sum(p.get("chunk_count", 0)
                      for p in st.session_state.papers.values()))
            c3.metric("Vectors in Pinecone", sum(p.get("vectors_upserted", 0)
                      for p in st.session_state.papers.values()))
            c4.metric("Figures Extracted", sum(len(p.get("figures", []))
                      for p in st.session_state.papers.values()))

            # Dataset stats
            if st.session_state.get("dataset"):
                st.markdown("<div style='height:12px'></div>",
                            unsafe_allow_html=True)
                ds_rows = len(st.session_state.dataset)
                dc1, dc2 = st.columns(2)
                dc1.metric("Dataset Rows", ds_rows)
                ds_name = st.session_state.get("dataset_filename", "N/A")
                dc2.metric("Dataset File", ds_name)

    # ──────────────────────────────────────────
    # EVALUATE TAB
    # ──────────────────────────────────────────
    with tab_evaluate:
        if selected == 'Evaluate':
            dataset = st.session_state.get("dataset")
            if not dataset:
                st.markdown("""
                <div style="text-align:center; padding:48px; color:var(--muted);">
                    <div style="font-size:32px; margin-bottom:8px;">📊</div>
                    <div style="font-size:14px; color:var(--text);">No dataset loaded.</div>
                    <div style="font-size:12px; margin-top:6px; color:var(--soft);">Upload a CSV or JSON dataset with question/answer pairs to run automatic evaluation.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    "<span class='section-label'>Automatic Evaluation</span>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<div style='font-size:13px; color:var(--muted); margin-bottom:16px;'>"
                    f"Run each question from your dataset through the RAG pipeline and compare answers to gold standard.</div>",
                    unsafe_allow_html=True)

                # Filter to rows with both question and answer
                eval_rows = [
                    r for r in dataset
                    if r.get("question", "").strip() and r.get("answer", "").strip()
                ]
                st.markdown(
                    f"<div style='font-size:13px; color:var(--text); margin-bottom:12px;'>"
                    f"<strong>{len(eval_rows)}</strong> evaluable question-answer pairs found.</div>",
                    unsafe_allow_html=True)

                # Max questions slider
                max_eval = st.slider(
                    "Max questions to evaluate",
                    min_value=1,
                    max_value=min(len(eval_rows), 50),
                    value=min(len(eval_rows), 10),
                    key="eval_max_questions",
                )

                if st.button("▶ Run Evaluation", use_container_width=True):
                    _run_evaluation(eval_rows[:max_eval])

                # Display previous results if available
                eval_results = st.session_state.get("eval_results")
                if eval_results:
                    _display_eval_results(eval_results)


def _run_evaluation(eval_rows: list[dict]):
    """Run the evaluation pipeline on selected rows."""
    from src.evaluation import (compute_aggregate_metrics, evaluate_single)
    from src.llm_qa import answer_question
    from src.rag_pipeline import semantic_search

    results = []
    progress_bar = st.progress(0.0)
    status_text = st.empty()

    source_mode = st.session_state.get("source_mode", "both")
    sf = None
    if source_mode == "pdf":
        sf = "pdf"
    elif source_mode == "dataset":
        sf = "dataset"

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
        )

        result = evaluate_single(
            question=question,
            gold_answer=gold_answer,
            model_answer=response.answer,
            embedder=st.session_state.embedder,
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


def _display_eval_results(eval_data: dict):
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

    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Mean F1 Score", f"{aggregate.get('mean_f1', 0):.2%}")
    mc2.metric("Mean Semantic Similarity", f"{aggregate.get('mean_semantic', 0):.2%}")
    mc3.metric("Questions Evaluated", aggregate.get("count", 0))

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

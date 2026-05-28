import streamlit as st

from src.rag_pipeline import semantic_search
from src.stream_helpers import render_question_turn


def populate_tabs(tab_chat, tab_figures, tab_search, tab_stats):
    # Chat tab
    with tab_chat:
        if not st.session_state.messages:
            st.markdown(
                "<span class='section-label'>Try these questions</span>", unsafe_allow_html=True)
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
                            "<div class='fig-match-banner'>📌 Related Figures from Paper</div>", unsafe_allow_html=True)
                        fig_cols = st.columns(len(saved_figs))
                        for col, fig in zip(fig_cols, saved_figs):
                            with col:
                                caption = f"{fig.fig_label}"
                                if fig.caption:
                                    caption += f" — {fig.caption}"
                                st.image(
                                    f"data:image/png;base64,{fig.image_base64}", caption=caption, width="stretch")
                    if "sources" in msg:
                        with st.expander(f"📎 {len(msg['sources'])} source chunks retrieved"):
                            for src in msg["sources"]:
                                st.markdown(f"""
                                <div class="source-chunk">
                                    <span class="score-badge">score: {src['score']}</span>
                                    &nbsp; chunk #{src['chunk_index']}<br/><br/>
                                    {src['text'][:300]}...
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
            render_question_turn(quick_question, st.session_state.active_paper_id, st.session_state.papers.get(
                st.session_state.active_paper_id, {}).get("figures", []))
            st.rerun()

        if prompt := st.chat_input("Ask anything about this paper..."):
            render_question_turn(prompt, st.session_state.active_paper_id, st.session_state.papers.get(
                st.session_state.active_paper_id, {}).get("figures", []))

        if st.session_state.messages:
            if st.button("🗑 Clear Chat"):
                st.session_state.messages = []
                st.rerun()

    # Figures tab
    with tab_figures:
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
                f"<div style='padding:8px 0 12px 0; font-size:13px; color:var(--muted);'>{len(paper_figures)} figures extracted · Search or browse all</div>", unsafe_allow_html=True)
            display_figs = paper_figures
            for i in range(0, len(display_figs), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    if i + j < len(display_figs):
                        fig = display_figs[i + j]
                        with col:
                            with st.container():
                                st.markdown(f"""
                                <div class="fig-card"><div class="fig-label">{fig.fig_label} · Page {fig.page}</div><div class="fig-caption">{fig.caption if fig.caption else "No caption detected"}</div></div>
                                """, unsafe_allow_html=True)
                                st.image(
                                    f"data:image/png;base64,{fig.image_base64}", width="stretch")
                                st.markdown(
                                    "<div style='height:8px'></div>", unsafe_allow_html=True)

    # Search tab
    with tab_search:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<span class='sec-label'>Search paper chunks by semantic similarity</span>", unsafe_allow_html=True)
        search_col, k_col = st.columns([4, 1])
        with search_col:
            search_query = st.text_input(
                "Search Query", placeholder="e.g. attention mechanism, loss function, dataset...", label_visibility="collapsed")
        with k_col:
            top_k = st.selectbox(
                "Top K", [3, 5, 8, 10], index=1, label_visibility="collapsed")
        if search_query:
            with st.spinner("Searching..."):
                results = semantic_search(query=search_query, embedder=st.session_state.embedder,
                                          index=st.session_state.index, top_k=top_k, filter_paper_id=st.session_state.active_paper_id)
            st.markdown(
                f"<div style='font-size:12px; color:var(--muted); margin:10px 0;'>Found {len(results)} chunks</div>", unsafe_allow_html=True)
            for r in results:
                score_pct = int(r["score"] * 100)
                with st.expander(f"Chunk #{r['chunk_index']} — Score: {r['score']} ({score_pct}% match)"):
                    st.progress(r["score"])
                    st.markdown(f"""
                    <div class="source-chunk" style="max-height:300px; overflow-y:auto;">{r['text']}</div>""", unsafe_allow_html=True)

    # Stats tab
    with tab_stats:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Papers Indexed", len(st.session_state.papers))
        c2.metric("Total Chunks", sum(p.get("chunk_count", 0)
                  for p in st.session_state.papers.values()))
        c3.metric("Vectors in Pinecone", sum(p.get("vectors_upserted", 0)
                  for p in st.session_state.papers.values()))
        c4.metric("Figures Extracted", sum(len(p.get("figures", []))
                  for p in st.session_state.papers.values()))

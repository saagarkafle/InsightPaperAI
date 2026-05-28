import json
import os
from dataclasses import asdict

import streamlit as st

from src.llm_qa import answer_question, generate_paper_summary, get_groq_client
from src.pdf_parser import Figure, find_relevant_figures, parse_paper
from src.rag_pipeline import (chunk_text, get_embedder, get_pinecone_index,
                              make_paper_id, semantic_search, upsert_paper)
from src.state import save_app_state


@st.cache_resource
def init_clients():
    embedder = get_embedder()
    index = get_pinecone_index("research-papers")
    groq = get_groq_client()
    return embedder, index, groq


def render_question_turn(prompt: str, active_paper_id: str, paper_figures: list) -> None:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="📚"):
        with st.spinner("Retrieving relevant sections..."):
            chunks = semantic_search(
                query=prompt,
                embedder=st.session_state.embedder,
                index=st.session_state.index,
                top_k=5,
                filter_paper_id=active_paper_id,
            )
        with st.spinner("Generating answer..."):
            response = answer_question(
                question=prompt,
                retrieved_chunks=chunks,
                client=st.session_state.groq_client,
            )

        st.markdown(response.answer)

        matched_figs = find_relevant_figures(prompt, paper_figures, top_k=2)
        if matched_figs:
            st.markdown(
                "<div class='fig-match-banner'>📌 Related Figures from Paper</div>",
                unsafe_allow_html=True,
            )
            fig_cols = st.columns(len(matched_figs))
            for col, fig in zip(fig_cols, matched_figs):
                with col:
                    caption = f"{fig.fig_label}"
                    if fig.caption:
                        caption += f" — {fig.caption}"
                    st.image(
                        f"data:image/png;base64,{fig.image_base64}",
                        caption=caption,
                        width="stretch",
                    )

        with st.expander(f"📎 {len(chunks)} source chunks retrieved"):
            for src in chunks:
                st.markdown(f"""
                <div class="source-chunk">
                    <span class="score-badge">score: {src['score']}</span>
                    &nbsp; chunk #{src['chunk_index']}<br/><br/>
                    {src['text'][:300]}...
                </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Latency", f"{response.latency_ms:.0f}ms")
        c2.metric("Tokens", f"{response.tokens_in}→{response.tokens_out}")
        c3.metric("Sources", len(chunks))

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.answer,
        "sources": chunks,
        "matched_figures": matched_figs,
        "meta": {
            "latency_ms": response.latency_ms,
            "tokens_in": response.tokens_in,
            "tokens_out": response.tokens_out,
        },
    })
    save_app_state(st.session_state)

import os
import time

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import streamlit as st

from src.llm_qa import answer_question, generate_paper_summary, get_groq_client
from src.pdf_parser import parse_paper
from src.rag_pipeline import chunk_text, get_embedder, get_pinecone_index, make_paper_id, semantic_search
from src.ui.styles import FLAT_CSS

# ==========================================
# PAGE CONFIG & CSS
# ==========================================
st.set_page_config(
    page_title="InsightPaper AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(FLAT_CSS, unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.embedder = get_embedder()
    st.session_state.index = get_pinecone_index()
    st.session_state.groq_client = get_groq_client()
    st.session_state.pdf_text = ""
    st.session_state.pdf_chunk_count = 0
    st.session_state.paper_summary = None
    st.session_state.active_paper_id = None
    st.session_state.messages = []

# ==========================================
# TITLE
# ==========================================
st.markdown("<h1>InsightPaper AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 14px; margin-top: -10px;'>Ask questions grounded in your research</p>", unsafe_allow_html=True)
st.divider()

# ==========================================
# PDF UPLOAD (hide after loaded)
# ==========================================
if not st.session_state.active_paper_id:
    pdf_upload = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"], key="pdf_up")
    if pdf_upload:
        with st.spinner("Parsing, indexing, and summarizing PDF..."):
            paper = parse_paper(pdf_upload, pdf_upload.name)
            chunks = chunk_text(paper.full_text)
            paper_id = make_paper_id(pdf_upload.name)
            from src.rag_pipeline import upsert_paper
            upsert_paper(
                paper_id=paper_id,
                paper_title=paper.title,
                chunks=chunks,
                embedder=st.session_state.embedder,
                index=st.session_state.index,
                source_type="pdf"
            )
            summary = generate_paper_summary(
                paper.full_text, st.session_state.groq_client)
            st.session_state.pdf_text = paper.full_text
            st.session_state.pdf_chunk_count = len(chunks)
            st.session_state.active_paper_id = pdf_upload.name
            st.session_state.paper_summary = summary
            st.rerun()
else:
    # Show loaded status and option to change
    col_status, col_btn = st.columns([4, 1])
    with col_status:
        st.markdown(f"✓ **{st.session_state.active_paper_id}** loaded")
    with col_btn:
        if st.button("New paper"):
            st.session_state.active_paper_id = None
            st.session_state.pdf_text = ""
            st.session_state.pdf_chunk_count = 0
            st.session_state.paper_summary = None
            st.session_state.messages = []
            st.rerun()

    # -- Summary & Key Points --
    summary = st.session_state.paper_summary
    if summary:
        with st.expander("Paper Summary & Key Points", expanded=False):
            one_liner = summary.get("one_liner", "")
            problem = summary.get("problem", "")
            approach = summary.get("approach", "")
            findings = summary.get("key_findings", [])
            limitations = summary.get("limitations", [])
            keywords = summary.get("keywords", [])
            difficulty = summary.get("difficulty", "")
            field = summary.get("field", "")

            if one_liner:
                st.markdown(f"**Summary:** {one_liner}")
            if problem:
                st.markdown(f"**Problem:** {problem}")
            if approach:
                st.markdown(f"**Approach:** {approach}")
            if findings:
                st.markdown("**Key Findings:**")
                for f in findings:
                    st.markdown(f"- {f}")
            if limitations:
                st.markdown("**Limitations:**")
                for lim in limitations:
                    st.markdown(f"- {lim}")
            if keywords:
                st.markdown(f"**Keywords:** {', '.join(keywords)}")
            if difficulty or field:
                parts = []
                if difficulty:
                    parts.append(f"Difficulty: {difficulty}")
                if field:
                    parts.append(f"Field: {field}")
                st.markdown(f"*{' · '.join(parts)}*")

    st.divider()

    # ==========================================
    # CHAT INTERFACE (only shown after PDF is loaded)
    # ==========================================

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("meta"):
                st.markdown(
                    f"<p style='color: #6B7280; font-style: italic; font-size: 12px;'>"
                    f"Chunks: {msg['meta']['chunks_used']} · Latency: {msg['meta']['latency']:.1f}s</p>",
                    unsafe_allow_html=True
                )

    # Chat input
    if prompt := st.chat_input("Ask anything about this paper..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chunks = semantic_search(
                    query=prompt,
                    embedder=st.session_state.embedder,
                    index=st.session_state.index,
                    top_k=5,
                    source_filter="pdf"
                )

                response = answer_question(
                    question=prompt,
                    retrieved_chunks=chunks,
                    client=st.session_state.groq_client
                )

            st.markdown(response.answer)
            st.markdown(
                f"<p style='color: #6B7280; font-style: italic; font-size: 12px;'>"
                f"Chunks: {len(chunks)} · Latency: {response.latency_ms / 1000.0:.1f}s</p>",
                unsafe_allow_html=True
            )

        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.answer,
            "meta": {
                "chunks_used": len(chunks),
                "latency": response.latency_ms / 1000.0,
            }
        })
        st.rerun()

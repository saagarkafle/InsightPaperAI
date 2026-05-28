import os

import streamlit as st

from src.llm_qa import generate_paper_summary
from src.pdf_parser import parse_paper
from src.rag_pipeline import chunk_text, make_paper_id, upsert_paper
from src.state import APP_STATE_FILE, save_app_state
from src.stream_helpers import init_clients


def render_landing():
    hero_left, hero_right = st.columns([1.35, 0.9], gap="large")

    with hero_left:
        st.markdown("""
        <div class="hero-card">
            <div class="panel-kicker">Research paper copilot</div>
            <div class="hero-title">Ask questions about any paper<br/><span class="hero-highlight">with a polished dark interface</span></div>
            <div class="hero-copy">Upload a PDF, let the app extract text and figures, then ask grounded questions with source citations and semantic search in a polished dark interface.</div>
            <div class="hero-actions"><span class="chip">Upload PDF</span><span class="chip">Semantic search</span><span class="chip">Figure matching</span><span class="chip">RAG stats</span></div>
            <div class="hero-badge-row"><span class="pill-tag">Pinecone</span><span class="pill-tag">Groq</span><span class="pill-tag">PyMuPDF</span><span class="pill-tag">LLaMA 3.1</span></div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
        <div class="panel upload-panel compact">
            <div class="panel-title">Start a session</div>
            <div class="upload-note">200MB per file • PDF only</div>
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload PDF", type=["pdf"], label_visibility="collapsed")
        st.markdown("""
            <div class="panel-copy" style="margin-top:10px;">The paper gets chunked, embedded, summarized, and indexed in one pass.</div>
        </div>
        """, unsafe_allow_html=True)

        if uploaded:
            if st.button("Process and index paper", use_container_width=True, disabled=st.session_state.processing):
                try:
                    st.session_state.processing = True
                    embedder, index, groq_client = init_clients()
                    st.session_state.embedder = embedder
                    st.session_state.index = index
                    st.session_state.groq_client = groq_client

                    with st.status("Processing paper...", expanded=True) as status:
                        st.write("Extracting text and figures from PDF...")
                        paper = parse_paper(uploaded, uploaded.name)

                        st.write(f"Chunking {paper.word_count:,} words...")
                        chunks = chunk_text(
                            paper.full_text, chunk_size=500, overlap=100)

                        st.write(
                            f"Generating embeddings for {len(chunks)} chunks...")
                        paper_id = make_paper_id(uploaded.name)
                        count = upsert_paper(
                            paper_id=paper_id, paper_title=paper.title, chunks=chunks, embedder=embedder, index=index)

                        st.write("Generating paper summary...")
                        summary = generate_paper_summary(
                            paper.full_text, groq_client)

                        fig_count = len(paper.figures)
                        status.update(
                            label=f"Paper indexed. {fig_count} figures extracted.", state="complete")

                    st.session_state.papers[paper_id] = {
                        "title": paper.title,
                        "filename": uploaded.name,
                        "word_count": paper.word_count,
                        "chunk_count": len(chunks),
                        "vectors_upserted": count,
                        "summary": summary,
                        "figures": paper.figures,
                    }
                    st.session_state.active_paper_id = paper_id
                    st.session_state.messages = []
                    save_app_state(st.session_state)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    st.session_state.processing = False

    st.markdown("""
    <div style="height:14px"></div>
    <div class="panel">
        <div class="panel-title">What happens next</div>
        <div class="library-item active"><div class="library-label">Step 1</div><div class="library-title">Parse PDF content</div><div class="library-meta">Text and figures are extracted with PyMuPDF.</div></div>
        <div class="library-item"><div class="library-label">Step 2</div><div class="library-title">Build retrieval context</div><div class="library-meta">Chunks are embedded and stored in Pinecone.</div></div>
        <div class="library-item"><div class="library-label">Step 3</div><div class="library-title">Ask follow-up questions</div><div class="library-meta">Answers stay grounded in the exact paper sections.</div></div>
    </div>
    """, unsafe_allow_html=True)

    flow = st.columns(4, gap="medium")
    steps = [
        ("Parse", "PDF text and figures extracted with PyMuPDF"),
        ("Chunk", "Text split into overlapping 500-word segments"),
        ("Embed", "Each chunk embedded into a 384-dim vector"),
        ("Retrieve", "Query finds top chunks plus matching figures"),
    ]
    for col, (title, desc) in zip(flow, steps):
        with col:
            st.markdown(f"""
            <div class="stat-panel">
                <div class="panel-kicker">{title}</div>
                <div class="panel-copy" style="margin-top:10px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

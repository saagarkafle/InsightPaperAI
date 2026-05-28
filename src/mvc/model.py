from __future__ import annotations

import os
from typing import Callable

import streamlit as st

from src.llm_qa import generate_paper_summary
from src.pdf_parser import parse_paper
from src.rag_pipeline import chunk_text, make_paper_id, upsert_paper
from src.state import APP_STATE_FILE, DEFAULTS, load_app_state, save_app_state
from src.stream_helpers import init_clients


class AppModel:
    def initialize(self) -> None:
        for key, value in DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value
        load_app_state(st.session_state)

    def has_papers(self) -> bool:
        return bool(st.session_state.papers)

    def ensure_clients(self) -> None:
        if st.session_state.embedder and st.session_state.index and st.session_state.groq_client:
            return

        embedder, index, groq_client = init_clients()
        st.session_state.embedder = embedder
        st.session_state.index = index
        st.session_state.groq_client = groq_client

    def process_uploaded_paper(self, uploaded_file, progress: Callable[[str], None]) -> None:
        self.ensure_clients()

        progress("Extracting text and figures from PDF...")
        paper = parse_paper(uploaded_file, uploaded_file.name)

        progress(f"Chunking {paper.word_count:,} words...")
        chunks = chunk_text(paper.full_text, chunk_size=500, overlap=100)

        progress(f"Generating embeddings for {len(chunks)} chunks...")
        paper_id = make_paper_id(uploaded_file.name)
        vector_count = upsert_paper(
            paper_id=paper_id,
            paper_title=paper.title,
            chunks=chunks,
            embedder=st.session_state.embedder,
            index=st.session_state.index,
        )

        progress("Generating paper summary...")
        summary = generate_paper_summary(
            paper.full_text, st.session_state.groq_client)

        st.session_state.papers[paper_id] = {
            "title": paper.title,
            "filename": uploaded_file.name,
            "word_count": paper.word_count,
            "chunk_count": len(chunks),
            "vectors_upserted": vector_count,
            "summary": summary,
            "figures": paper.figures,
        }
        st.session_state.active_paper_id = paper_id
        st.session_state.messages = []
        save_app_state(st.session_state)

    def reset_current_session(self) -> None:
        st.session_state.papers = {}
        st.session_state.active_paper_id = None
        st.session_state.messages = []
        try:
            if os.path.exists(APP_STATE_FILE):
                os.remove(APP_STATE_FILE)
        except Exception:
            pass

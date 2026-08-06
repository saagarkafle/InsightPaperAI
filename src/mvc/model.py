from __future__ import annotations

import os
from typing import Callable

import streamlit as st

from src.dataset_parser import (dataset_to_chunks, make_dataset_id,
                                parse_csv, parse_json_dataset,
                                validate_dataset)
from src.llm_qa import generate_paper_summary, resolve_model_id
from src.pdf_parser import parse_paper
from src.rag_pipeline import (chunk_text, make_paper_id, upsert_dataset,
                              upsert_paper)
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

    def has_dataset(self) -> bool:
        return bool(st.session_state.get("dataset"))

    def has_any_source(self) -> bool:
        """Return True if either a paper or dataset has been processed."""
        return self.has_papers() or self.has_dataset()

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
            source_type="pdf",
        )

        progress("Generating paper summary...")
        model_id = resolve_model_id(st.session_state.get("selected_model"))
        summary = generate_paper_summary(
            paper.full_text, st.session_state.groq_client, model=model_id)

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

    def process_uploaded_dataset(self, uploaded_file, progress: Callable[[str], None]) -> tuple[bool, str]:
        """
        Parse, validate, and index an uploaded CSV/JSON dataset.
        Returns (success, error_message).
        """
        self.ensure_clients()

        progress("Reading dataset file...")
        file_content = uploaded_file.read()
        filename = uploaded_file.name

        # Parse based on file type
        try:
            if filename.lower().endswith(".csv"):
                rows = parse_csv(file_content)
            elif filename.lower().endswith(".json"):
                rows = parse_json_dataset(file_content)
            else:
                return False, "Unsupported file type. Please upload a .csv or .json file."
        except Exception as e:
            return False, f"Failed to parse file: {e}"

        # Validate
        is_valid, error_msg = validate_dataset(rows)
        if not is_valid:
            return False, error_msg

        progress(f"Found {len(rows)} rows in dataset.")

        # Extract chunks from context/answer fields
        chunks = dataset_to_chunks(rows)
        if not chunks:
            return False, "No indexable content found in dataset rows."

        progress(f"Indexing {len(chunks)} chunks into Pinecone...")
        dataset_id = make_dataset_id(filename)
        vector_count = upsert_dataset(
            dataset_id=dataset_id,
            dataset_name=filename,
            chunks=chunks,
            embedder=st.session_state.embedder,
            index=st.session_state.index,
        )

        # Store dataset in session state
        st.session_state.dataset = rows
        st.session_state.dataset_filename = filename
        st.session_state.dataset_id = dataset_id
        st.session_state.eval_results = None  # Clear previous eval results

        progress(f"Indexed {vector_count} dataset vectors.")
        save_app_state(st.session_state)
        return True, ""

    def reset_current_session(self) -> None:
        st.session_state.papers = {}
        st.session_state.active_paper_id = None
        st.session_state.messages = []
        # Clear dataset state
        st.session_state.dataset = None
        st.session_state.dataset_filename = None
        st.session_state.dataset_id = None
        st.session_state.source_mode = "both"
        st.session_state.eval_results = None
        try:
            if os.path.exists(APP_STATE_FILE):
                os.remove(APP_STATE_FILE)
        except Exception:
            pass

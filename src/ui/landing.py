import html as html_mod

import pandas as pd
import streamlit as st

from src.dataset_parser import get_preview_rows


def render_landing():
    """
    Render the landing screen with dual upload cards (PDF + Dataset),
    dataset preview, source mode toggle, and process button.
    Returns a dict with: uploaded_pdf, uploaded_dataset, process_requested.
    """
    uploaded_pdf = None
    uploaded_dataset = None
    process_requested = False

    hero_left, hero_right = st.columns([1.3, 0.95], gap="large")

    with hero_left:
        st.markdown("""
        <div class="hero-card">
            <div class="panel-kicker">Research paper copilot</div>
            <div class="hero-title">Ask questions about any paper<br/><span class="hero-highlight">with AI-powered analysis</span></div>
            <div class="hero-copy">Upload a PDF, let the app extract text and figures, then ask grounded questions with source citations and semantic search. You can also upload a custom dataset for evaluation.</div>
            <div class="hero-actions"><span class="chip">📄 Upload PDF</span><span class="chip">📊 Custom Dataset</span><span class="chip">🔍 Semantic search</span><span class="chip">📈 Auto Evaluation</span></div>
            <div class="hero-badge-row"><span class="pill-tag">Pinecone</span><span class="pill-tag">Groq</span><span class="pill-tag">PyMuPDF</span><span class="pill-tag">LLaMA 3.1</span></div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        # ─── PDF Upload Card ───
        st.markdown("""
        <div class="upload-card">
            <span class="upload-card-icon">📄</span>
            <div class="upload-card-title">Upload Research Paper</div>
            <div class="upload-card-desc">PDF files up to 200MB</div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_pdf = st.file_uploader(
            "Upload PDF", type=["pdf"], label_visibility="collapsed",
            key="landing_pdf_upload")

        # ─── Dataset Upload Card ───
        st.markdown("""
        <div class="upload-card">
            <span class="upload-card-icon">📊</span>
            <div class="upload-card-title">Upload Dataset (Optional)</div>
            <div class="upload-card-desc">CSV or JSON with question, answer, context columns</div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_dataset = st.file_uploader(
            "Upload Dataset", type=["csv", "json"], label_visibility="collapsed",
            key="landing_dataset_upload")

        # ─── Dataset Preview ───
        if uploaded_dataset:
            try:
                file_content = uploaded_dataset.read()
                uploaded_dataset.seek(0)  # Reset for later processing
                filename = uploaded_dataset.name

                if filename.lower().endswith(".csv"):
                    from src.dataset_parser import parse_csv
                    rows = parse_csv(file_content)
                else:
                    from src.dataset_parser import parse_json_dataset
                    rows = parse_json_dataset(file_content)

                preview = get_preview_rows(rows, n=5)
                if preview:
                    st.markdown(
                        "<span class='panel-title' style='border-bottom:none; padding-bottom:4px;'>Dataset Preview</span>",
                        unsafe_allow_html=True)
                    # Sanitize values for display
                    safe_preview = []
                    for row in preview:
                        safe_row = {}
                        for k, v in row.items():
                            safe_row[html_mod.escape(str(k))] = html_mod.escape(
                                str(v))[:120]
                        safe_preview.append(safe_row)
                    df = pd.DataFrame(safe_preview)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.caption(f"{len(rows)} total rows in dataset")
            except Exception as e:
                st.error(f"Could not preview dataset: {e}")

        # ─── Source Mode Toggle ───
        if uploaded_pdf and uploaded_dataset:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            source_mode = st.radio(
                "Source Mode",
                options=["Both", "PDF only", "Dataset only"],
                index=0,
                horizontal=True,
                key="landing_source_mode",
            )
            mode_map = {"Both": "both", "PDF only": "pdf", "Dataset only": "dataset"}
            st.session_state.source_mode = mode_map.get(source_mode, "both")

        # ─── Process Button ───
        if uploaded_pdf or uploaded_dataset:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            label = "Process & Index"
            if uploaded_pdf and uploaded_dataset:
                label = "Process PDF & Dataset"
            elif uploaded_pdf:
                label = "Process Paper"
            else:
                label = "Process Dataset"

            process_requested = st.button(
                label,
                use_container_width=True,
                disabled=st.session_state.processing,
            )

    # Steps panel
    st.markdown("""
    <div style="height:24px"></div>
    <div class="card">
        <div class="panel-title">How it works</div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
            <div class="card-flat"><div class="library-label">Step 1</div><div class="library-title">Parse & Extract</div><div class="library-meta">Text and figures are extracted from your PDF using PyMuPDF.</div></div>
            <div class="card-flat"><div class="library-label">Step 2</div><div class="library-title">Embed & Index</div><div class="library-meta">Chunks are embedded and stored in Pinecone for semantic retrieval.</div></div>
            <div class="card-flat"><div class="library-label">Step 3</div><div class="library-title">Ask & Evaluate</div><div class="library-meta">Ask questions with source citations, or auto-evaluate with your dataset.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return {
        "uploaded_pdf": uploaded_pdf,
        "uploaded_dataset": uploaded_dataset,
        "process_requested": process_requested,
    }

import streamlit as st


def render_landing():
    """
    Render the landing screen with a PDF upload card and process button.
    Returns a dict with: uploaded_pdf, uploaded_dataset, process_requested.
    """
    uploaded_pdf = None
    process_requested = False

    hero_left, hero_right = st.columns([1.3, 0.95], gap="large")

    with hero_left:
        st.markdown("""
        <div class="hero-card">
            <div class="panel-kicker">Research paper copilot</div>
            <div class="hero-title">Ask questions about any paper<br/><span class="hero-highlight">with AI-powered analysis</span></div>
            <div class="hero-copy">Upload a PDF, let the app extract text and figures, then ask grounded questions with source citations and semantic search.</div>
            <div class="hero-actions"><span class="chip">📄 Upload PDF</span><span class="chip">🔍 Semantic search</span><span class="chip">🖼 Figure extraction</span></div>
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

        # ─── Process Button ───
        if uploaded_pdf:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            process_requested = st.button(
                "Process Paper",
                use_container_width=True,
                disabled=st.session_state.processing,
            )

    # Steps panel
    st.markdown("""
    <div style="height:24px"></div>
    <div class="card">
        <div class="panel-title">How it works</div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
            <div class="card-flat"><div class="library-label">Step 1</div><div class="library-title">Parse &amp; Extract</div><div class="library-meta">Text and figures are extracted from your PDF using PyMuPDF.</div></div>
            <div class="card-flat"><div class="library-label">Step 2</div><div class="library-title">Embed &amp; Index</div><div class="library-meta">Chunks are embedded and stored in Pinecone for semantic retrieval.</div></div>
            <div class="card-flat"><div class="library-label">Step 3</div><div class="library-title">Ask Questions</div><div class="library-meta">Ask grounded questions with source citations and semantic search.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return {
        "uploaded_pdf": uploaded_pdf,
        "uploaded_dataset": None,
        "process_requested": process_requested,
    }

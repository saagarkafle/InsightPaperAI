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
            <div class="hero-badge-row"><span class="pill-tag">Pinecone</span><span class="pill-tag">Groq</span><span class="pill-tag">PyMuPDF</span><span class="pill-tag">Qwen 3.6 / LLaMA 3.1</span></div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        # ─── Model Selector ───
        from src.llm_qa import AVAILABLE_MODELS, DEFAULT_MODEL
        model_names = list(AVAILABLE_MODELS.keys())
        current_model = st.session_state.get("selected_model") or DEFAULT_MODEL
        try:
            model_idx = model_names.index(current_model)
        except ValueError:
            model_idx = 0

        st.markdown("<div style='font-size:13px; font-weight:700; color:var(--text-secondary); margin-bottom:4px;'>🤖 Select AI Model</div>", unsafe_allow_html=True)
        selected_model = st.selectbox(
            "Select AI Model",
            options=model_names,
            index=model_idx,
            key="landing_model_select",
            label_visibility="collapsed",
        )
        st.session_state.selected_model = selected_model

        # ─── Model guide hint ───
        if "Qwen" in selected_model:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(45,212,191,0.08), rgba(99,102,241,0.08));
                border: 1px solid rgba(45,212,191,0.25);
                border-radius: 10px;
                padding: 10px 14px;
                margin-top: 6px;
                font-size: 12px;
                color: var(--text-secondary);
                line-height: 1.5;
            ">
                <span style="font-weight:700; color:#2dd4bf;">🧠 Deep Analysis</span> — Best for detailed research questions,
                complex multi-part queries, and thorough paper summaries. Uses Qwen 3.6 27B via Groq.
                Slightly slower (~2 s), but produces richer, more complete answers.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.08));
                border: 1px solid rgba(99,102,241,0.25);
                border-radius: 10px;
                padding: 10px 14px;
                margin-top: 6px;
                font-size: 12px;
                color: var(--text-secondary);
                line-height: 1.5;
            ">
                <span style="font-weight:700; color:#818cf8;">⚡ Fast Inference</span> — Best for quick lookups,
                rapid iterative Q&amp;A, and simple factual questions. Uses LLaMA 3.1 8B via Groq.
                Very fast (~0.4 s), ideal when you want instant answers.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # ─── PDF Upload Card (styled as the file uploader itself) ───
        st.markdown("""
        <style>
        /* Expand & style the dropzone to look like the card */
        div.stFileUploader section[data-testid="stFileUploaderDropzone"] {
            padding: 22px 20px !important;
            border-radius: 14px !important;
            cursor: pointer !important;
            min-height: 110px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            transition: border-color 0.2s ease, background 0.2s ease !important;
            gap: 0 !important;
        }
        div.stFileUploader section[data-testid="stFileUploaderDropzone"]:hover {
            border-color: rgba(99,102,241,0.55) !important;
            background: rgba(99,102,241,0.04) !important;
        }
        /* PDF icon at top via pseudo-element */
        div.stFileUploader section[data-testid="stFileUploaderDropzone"]::before {
            content: "📄";
            font-size: 28px;
            line-height: 1;
            display: block;
            margin-bottom: 8px;
        }
        /* Hide Streamlit's default drag-and-drop instructions block */
        div[data-testid="stFileUploaderDropzoneInstructions"] {
            display: none !important;
        }
        /* Show our custom title + subtitle via ::after */
        div.stFileUploader section[data-testid="stFileUploaderDropzone"]::after {
            content: "Upload Research Paper\\A PDF files up to 200MB";
            white-space: pre;
            display: block;
            text-align: center;
            font-weight: 700;
            font-size: 14px;
            line-height: 2;
            color: inherit;
            opacity: 0.85;
        }
        /* Hide the "Browse files" / "Upload" button */
        div.stFileUploader section[data-testid="stFileUploaderDropzone"] > button {
            display: none !important;
        }
        /* Hide ALL remaining children (SVG icon, any stray text nodes, etc.) */
        div.stFileUploader section[data-testid="stFileUploaderDropzone"] > * {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        uploaded_pdf = st.file_uploader(
            "Upload PDF", type=["pdf"], label_visibility="collapsed",
            key="landing_pdf_upload")

        # ─── Process Button (always visible, disabled until paper is uploaded) ───
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        process_requested = st.button(
            "Process Paper",
            use_container_width=True,
            disabled=(not uploaded_pdf) or st.session_state.processing,
        )

    # Steps panel
    st.markdown("""
    <div style="height:8px"></div>
    <div class="card">
        <div class="panel-title">How it works</div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:16px;">
            <div class="card-flat"><div class="library-label">Step 1</div><div class="library-title">📄 Upload PDF</div><div class="library-meta">Select any research paper PDF. The app accepts files up to 200 MB.</div></div>
            <div class="card-flat"><div class="library-label">Step 2</div><div class="library-title">🔍 Parse &amp; Extract</div><div class="library-meta">Text blocks and embedded figures are extracted page-by-page using PyMuPDF.</div></div>
            <div class="card-flat"><div class="library-label">Step 3</div><div class="library-title">🧩 Chunk &amp; Embed</div><div class="library-meta">Text is split into overlapping 500-word chunks and encoded into 384-d dense vectors.</div></div>
            <div class="card-flat"><div class="library-label">Step 4</div><div class="library-title">🗄️ Index in Pinecone</div><div class="library-meta">Vectors are upserted into Pinecone with metadata for fast cosine similarity retrieval.</div></div>
            <div class="card-flat"><div class="library-label">Step 5</div><div class="library-title">💬 Ask Questions</div><div class="library-meta">Ask anything in natural language. The top-5 chunks are retrieved and fed to the LLM as grounded context.</div></div>
            <div class="card-flat"><div class="library-label">Step 6</div><div class="library-title">📊 Evaluate &amp; Benchmark</div><div class="library-meta">Upload a Q&amp;A dataset to auto-score answers using Token F1, Semantic Similarity, and LLM-as-a-Judge.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return {
        "uploaded_pdf": uploaded_pdf,
        "uploaded_dataset": None,
        "process_requested": process_requested,
    }

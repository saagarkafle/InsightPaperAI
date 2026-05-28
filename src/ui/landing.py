import streamlit as st


def render_landing():
    uploaded = None
    process_requested = False
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
        """, unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload PDF", type=["pdf"], label_visibility="collapsed")
        st.markdown("""
            <div class="panel-copy" style="margin-top:10px;">The paper gets chunked, embedded, summarized, and indexed in one pass.</div>
        </div>
        """, unsafe_allow_html=True)

        if uploaded:
            process_requested = st.button(
                "Process and index paper",
                use_container_width=True,
                disabled=st.session_state.processing,
            )

    st.markdown("""
    <div style="height:24px"></div>
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

    return uploaded, process_requested

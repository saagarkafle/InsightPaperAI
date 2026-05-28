# app.py — Research Paper Q&A Engine (RAG)
from src.llm_qa import get_groq_client, answer_question, generate_paper_summary
from src.rag_pipeline import (
    get_embedder, get_pinecone_index, chunk_text,
    upsert_paper, semantic_search, make_paper_id, delete_paper
)
from dataclasses import asdict
from src.pdf_parser import parse_paper, find_relevant_figures, Figure
import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud secrets support
try:
    for key in ["GEMINI_API_KEY", "PINECONE_API_KEY", "GROQ_API_KEY"]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass


# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="InsightPaper AI — Research Q&A",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #121212;
    --panel: #181818;
    --panel-2: #202020;
    --line: #2f2f2f;
    --text: #f5f5f5;
    --muted: #b3b3b3;
    --soft: #9ca3af;
    --green: #1db954;
    --green-2: #169c46;
    --shadow: 0 18px 50px rgba(0, 0, 0, 0.38);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background:
        radial-gradient(circle at top left, rgba(29, 185, 84, 0.12), transparent 26%),
        radial-gradient(circle at 90% 10%, rgba(29, 185, 84, 0.08), transparent 20%),
        linear-gradient(180deg, #0f0f0f 0%, #111111 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text);
}

.stApp > header { background: transparent !important; }

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 18px 24px;
    margin: -1rem -1rem 20px -1rem;
    background: rgba(18, 18, 18, 0.92);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    position: sticky;
    top: 0;
    z-index: 100;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #3df168, var(--green));
    box-shadow: 0 0 0 8px rgba(29, 185, 84, 0.08);
    display: grid;
    place-items: center;
    color: #0f0f0f;
    font-weight: 900;
    font-size: 18px;
}

.brand-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.4px;
}

.brand-subtitle {
    font-size: 12px;
    color: var(--muted);
    margin-top: 2px;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
}

.hero-card,
.panel,
.mini-panel,
.stat-panel,
.paper-card,
.card,
.card-glow,
.fig-card,
.source-chunk {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02)) !important;
    border-radius: 22px !important;
    box-shadow: var(--shadow);
}

.hero-card {
    position: relative;
    overflow: hidden;
    padding: 28px;
    background:
        radial-gradient(circle at top right, rgba(29, 185, 84, 0.22), transparent 28%),
        linear-gradient(145deg, #222222 0%, #171717 50%, #131313 100%) !important;
}

.hero-title {
    font-size: clamp(34px, 5vw, 62px);
    font-weight: 800;
    line-height: 0.96;
    letter-spacing: -2px;
    margin: 12px 0 16px 0;
    color: var(--text);
}

.hero-highlight { color: var(--green); }

.hero-copy {
    max-width: 700px;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.7;
}

.hero-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 22px;
}

.hero-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 18px;
}

.panel { padding: 22px; background: linear-gradient(180deg, #1f1f1f 0%, #161616 100%) !important; }
.panel.compact { padding: 16px; }

.panel-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
}

.panel-kicker {
    color: var(--green);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.panel-copy {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.65;
}

.upload-panel { padding: 22px; }
.upload-panel .stFileUploader { padding-top: 8px; }
.upload-note { color: var(--muted); font-size: 12px; line-height: 1.5; margin-top: 4px; }

.stat-panel {
    padding: 18px;
    margin-bottom: 14px;
}

.library-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 14px 16px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 10px;
}

.library-item.active {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.18), rgba(255, 255, 255, 0.04));
    border-color: rgba(29, 185, 84, 0.38);
}

.library-label {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    font-weight: 700;
}

.library-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 600;
    line-height: 1.4;
}

.library-meta {
    color: var(--soft);
    font-size: 12px;
}

.sec-label,
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--muted);
    display: block;
    margin-bottom: 12px;
}

.paper-card {
    padding: 16px 18px;
    margin: 8px 0;
    background: rgba(255, 255, 255, 0.035) !important;
    border-left: 4px solid rgba(29, 185, 84, 0.65) !important;
}

.paper-card.active {
    border-left-color: var(--green) !important;
    background: rgba(29, 185, 84, 0.11) !important;
}

.overview-grid {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 16px;
    align-items: start;
}

.overview-grid > div {
    min-width: 0;
}

.overview-copy {
    color: #d7d7d7;
    font-size: 15px;
    line-height: 1.7;
}

.findings-stack {
    padding-right: 4px;
}

.kw-tag,
.pill-tag {
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    margin: 3px 4px 3px 0;
    border-radius: 999px;
    background: rgba(29, 185, 84, 0.12);
    color: #dff7e6;
    border: 1px solid rgba(29, 185, 84, 0.22);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2px;
}

.finding-item {
    padding: 11px 14px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    margin: 8px 0;
    font-size: 13px;
    color: #e2e2e2;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.source-chunk {
    padding: 14px 16px;
    margin: 8px 0;
    font-size: 12px;
    color: #cfcfcf;
    line-height: 1.65;
    background: rgba(255, 255, 255, 0.04) !important;
}

.score-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(29, 185, 84, 0.16);
    color: #dff7e6;
    border: 1px solid rgba(29, 185, 84, 0.24);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}

.diff-beginner,
.diff-intermediate,
.diff-advanced {
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2px;
}
.diff-beginner { color: #07240f; background: #1db954; border: 1px solid #31d366; }
.diff-intermediate { color: #f5f5f5; background: #5d5d5d; border: 1px solid #737373; }
.diff-advanced { color: #fff; background: #3b3b3b; border: 1px solid #5a5a5a; }

.fig-card {
    padding: 16px;
    margin-bottom: 14px;
    background: rgba(255, 255, 255, 0.035) !important;
}

.fig-label {
    font-size: 11px;
    font-weight: 800;
    color: var(--green);
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.fig-caption {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.6;
    margin-bottom: 10px;
}

.fig-match-banner {
    background: rgba(29, 185, 84, 0.12);
    border: 1px solid rgba(29, 185, 84, 0.2);
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 800;
    color: #dff7e6;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 14px 0 10px 0;
}

.stat-card {
    padding: 16px;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.stat-value {
    font-size: 24px;
    font-weight: 800;
    color: var(--text);
    line-height: 1.1;
}

.stat-label {
    margin-top: 6px;
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    font-weight: 700;
}

.stat-note {
    margin-top: 10px;
    color: var(--soft);
    font-size: 12px;
    line-height: 1.5;
}

.footer-bar {
    margin-top: 24px;
    padding: 18px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    color: var(--muted);
    font-size: 12px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}

.stButton > button {
    background: linear-gradient(135deg, var(--green), var(--green-2)) !important;
    color: #0f0f0f !important;
    border: none !important;
    border-radius: 999px !important;
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 14px 30px rgba(29, 185, 84, 0.2) !important;
    opacity: 0.96 !important;
}

[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 18px !important;
    margin-bottom: 12px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(29, 185, 84, 0.08) !important;
    border-color: rgba(29, 185, 84, 0.22) !important;
}
[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 18px !important;
}
[data-testid="stChatInput"]:focus-within { border-color: rgba(29, 185, 84, 0.7) !important; }
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border-radius: 14px !important;
    padding: 2px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    border: none !important;
    padding: 6px 10px !important;
    min-height: 32px !important;
    line-height: 1 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(29, 185, 84, 0.16) !important;
    color: var(--text) !important;
}

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.035) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 18px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 22px !important;
    font-weight: 800 !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--green), #3df168) !important;
    border-radius: 999px !important;
}

hr { border-color: rgba(255, 255, 255, 0.08) !important; margin: 20px 0 !important; }
#MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #121212; }
::-webkit-scrollbar-thumb { background: #3a3a3a; border-radius: 999px; }
[data-testid="stSuccess"] { background: rgba(29, 185, 84, 0.12) !important; border: 1px solid rgba(29, 185, 84, 0.24) !important; border-radius: 14px !important; }
[data-testid="stError"] { background: rgba(239, 68, 68, 0.12) !important; border: 1px solid rgba(239, 68, 68, 0.24) !important; border-radius: 14px !important; }
[data-testid="stInfo"] { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 14px !important; }
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
    color: var(--text) !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploader"] > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1.5px dashed rgba(29, 185, 84, 0.35) !important;
    border-radius: 18px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
DEFAULTS = {
    "papers": {},
    "active_paper_id": None,
    "messages": [],
    "embedder": None,
    "index": None,
    "groq_client": None,
    "processing": False,
    "initialized": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

APP_STATE_FILE = os.path.join(os.path.dirname(
    __file__), ".insightpaper_state.json")


def _serialize_papers(papers: dict) -> dict:
    serialized = {}
    for paper_id, paper in papers.items():
        paper_copy = dict(paper)
        paper_copy["figures"] = [
            asdict(fig) if hasattr(fig, "fig_label") else fig
            for fig in paper_copy.get("figures", [])
        ]
        serialized[paper_id] = paper_copy
    return serialized


def _deserialize_papers(papers: dict) -> dict:
    restored = {}
    for paper_id, paper in papers.items():
        paper_copy = dict(paper)
        paper_copy["figures"] = [
            Figure(**fig) if isinstance(fig, dict) else fig
            for fig in paper_copy.get("figures", [])
        ]
        restored[paper_id] = paper_copy
    return restored


def save_app_state() -> None:
    payload = {
        "papers": _serialize_papers(st.session_state.papers),
        "active_paper_id": st.session_state.active_paper_id,
    }
    try:
        with open(APP_STATE_FILE, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except Exception:
        pass


def load_app_state() -> None:
    if not os.path.exists(APP_STATE_FILE):
        return
    try:
        with open(APP_STATE_FILE, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        st.session_state.papers = _deserialize_papers(
            payload.get("papers", {}))
        st.session_state.active_paper_id = payload.get("active_paper_id")
        if st.session_state.active_paper_id not in st.session_state.papers:
            st.session_state.active_paper_id = next(
                iter(st.session_state.papers), None)
    except Exception:
        pass


load_app_state()


# ═══════════════════════════════════════════════════════
# INIT CLIENTS (cached)
# ═══════════════════════════════════════════════════════
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
    save_app_state()


# ═══════════════════════════════════════════════════════
# NAVBAR
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
    <div class="brand">
        <div class="brand-mark">I</div>
        <div>
            <div class="brand-title">InsightPaper AI</div>
            <div class="brand-subtitle">Research paper Q&A</div>
        </div>
    </div>
    <div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end;">
        <span class="chip">🟢 RAG pipeline</span>
        <span class="chip">📎 Source citations</span>
        <span class="chip">🧠 Groq + Pinecone</span>
    </div>
</div>
<div style="height:6px"></div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════
if not st.session_state.papers:
    hero_left, hero_right = st.columns([1.35, 0.9], gap="large")

    with hero_left:
        st.markdown("""
        <div class="hero-card">
            <div class="panel-kicker">Research paper copilot</div>
            <div class="hero-title">Ask questions about any paper<br/><span class="hero-highlight">with a polished dark interface</span></div>
            <div class="hero-copy">
                Upload a PDF, let the app extract text and figures, then ask grounded questions with source citations and semantic search in a polished dark interface.
            </div>
            <div class="hero-actions">
                <span class="chip">Upload PDF</span>
                <span class="chip">Semantic search</span>
                <span class="chip">Figure matching</span>
                <span class="chip">RAG stats</span>
            </div>
            <div class="hero-badge-row">
                <span class="pill-tag">Pinecone</span>
                <span class="pill-tag">Groq</span>
                <span class="pill-tag">PyMuPDF</span>
                <span class="pill-tag">LLaMA 3.1</span>
            </div>
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
            <div class="panel-copy" style="margin-top:10px;">
                The paper gets chunked, embedded, summarized, and indexed in one pass.
            </div>
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
                            paper_id=paper_id,
                            paper_title=paper.title,
                            chunks=chunks,
                            embedder=embedder,
                            index=index
                        )

                        st.write("Generating paper summary...")
                        summary = generate_paper_summary(
                            paper.full_text, groq_client)

                        fig_count = len(paper.figures)
                        status.update(
                            label=f"Paper indexed. {fig_count} figures extracted.",
                            state="complete"
                        )

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
                    save_app_state()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    st.session_state.processing = False

        st.markdown("""
        <div style="height:14px"></div>
        <div class="panel">
            <div class="panel-title">What happens next</div>
            <div class="library-item active">
                <div class="library-label">Step 1</div>
                <div class="library-title">Parse PDF content</div>
                <div class="library-meta">Text and figures are extracted with PyMuPDF.</div>
            </div>
            <div class="library-item">
                <div class="library-label">Step 2</div>
                <div class="library-title">Build retrieval context</div>
                <div class="library-meta">Chunks are embedded and stored in Pinecone.</div>
            </div>
            <div class="library-item">
                <div class="library-label">Step 3</div>
                <div class="library-title">Ask follow-up questions</div>
                <div class="library-meta">Answers stay grounded in the exact paper sections.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

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


# ═══════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════════
else:
    if not st.session_state.embedder:
        try:
            embedder, index, groq_client = init_clients()
            st.session_state.embedder = embedder
            st.session_state.index = index
            st.session_state.groq_client = groq_client
        except Exception as e:
            st.error(f"Client init error: {e}")
            st.stop()

    active_id = st.session_state.active_paper_id
    active_paper = st.session_state.papers.get(active_id, {})
    summary = active_paper.get("summary", {})
    paper_figures = active_paper.get("figures", [])

    dashboard_main, dashboard_right = st.columns([2.8, 0.72], gap="large")

    with dashboard_main:
        fig_count = len(paper_figures)
        st.markdown(f"""
        <div class="hero-card" style="margin-bottom:18px;">
            <div class="panel-kicker">Now reading</div>
            <div style="font-size:26px; font-weight:800; color:var(--text); margin-top:8px; line-height:1.2; letter-spacing:-0.9px;">
                {active_paper.get('title', 'Research Paper')[:90]}
            </div>
            <div class="hero-copy" style="margin-top:12px; max-width:none;">
                {active_paper.get('filename', '')} · {active_paper.get('word_count', 0):,} words · {active_paper.get('chunk_count', 0)} chunks · {active_paper.get('vectors_upserted', 0)} vectors · {fig_count} figures extracted
            </div>
        </div>
        """, unsafe_allow_html=True)

        if summary:
            one_liner = summary.get("one_liner", "")
            problem = summary.get("problem", "")
            approach = summary.get("approach", "")
            diff = summary.get("difficulty", "Intermediate")
            field = summary.get("field", "")
            diff_class = f"diff-{diff.lower()}"

            findings = summary.get("key_findings", [])
            keywords = summary.get("keywords", [])

            findings_html = "".join(
                f"<div class='finding-item'>• {f}</div>" for f in findings[:3]
            ) if findings else ""
            keywords_html = "".join(
                f"<span class='kw-tag'>{k}</span>" for k in keywords
            ) if keywords else ""

            st.markdown(f"""
            <div class="overview-grid">
                <div class="card-glow" style="padding:22px;">
                    <div class="panel-title">Paper overview</div>
                    <div class="overview-copy" style="margin-bottom:14px;">{one_liner}</div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;">
                        <span class="{diff_class}">{diff}</span>
                        <span class="pill-tag">{field}</span>
                    </div>
                    {"<div class='panel-copy' style='margin-bottom:8px;'><strong style='color:#f5f5f5;'>Problem:</strong> " + problem + "</div>" if problem else ""}
                    {"<div class='panel-copy'><strong style='color:#f5f5f5;'>Approach:</strong> " + approach + "</div>" if approach else ""}
                </div>
                <div class="panel">
                    <div class="panel-title">Key findings</div>
                    <div class="findings-stack">{findings_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if keywords_html:
                st.markdown("<div style='height:12px'></div>",
                            unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class="panel">
                        <div class="panel-title">Topics</div>
                        <div>{keywords_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        tab_chat, tab_figures, tab_search, tab_stats = st.tabs([
            "Ask Questions",
            f"Figures ({len(paper_figures)})",
            "Search",
            "Stats"
        ])

    with dashboard_right:
        st.markdown(
            f"""
            <div class="panel compact">
                <div class="panel-title">Your library</div>
                <div class="panel-copy" style="margin-bottom:12px;">Loaded paper</div>
            """,
            unsafe_allow_html=True,
        )
        for paper_id, paper in st.session_state.papers.items():
            active_class = " active" if paper_id == active_id else ""
            st.markdown(f"""
                <div class="library-item{active_class}">
                    <div class="library-title">{paper.get('title', 'Research Paper')[:72]}</div>
                    <div class="library-meta">{paper.get('chunk_count', 0)} chunks · {len(paper.get('figures', []))} figures</div>
                </div>
            """, unsafe_allow_html=True)
        if st.button("Research new paper", use_container_width=True):
            st.session_state.papers = {}
            st.session_state.active_paper_id = None
            st.session_state.messages = []
            try:
                if os.path.exists(APP_STATE_FILE):
                    os.remove(APP_STATE_FILE)
            except Exception:
                pass
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="panel compact">
                <div class="panel-title">Session stats</div>
                <div class="stat-card">
                    <div class="stat-value">{len(st.session_state.messages)}</div>
                    <div class="stat-label">Messages</div>
                </div>
                <div style="height:10px"></div>
                <div class="stat-card">
                    <div class="stat-value">{len(paper_figures)}</div>
                    <div class="stat-label">Figures</div>
                </div>
                <div style="height:10px"></div>
                <div class="stat-card">
                    <div class="stat-value">{active_paper.get('chunk_count', 0)}</div>
                    <div class="stat-label">Chunks</div>
                </div>
                <div class="stat-note">Use the center tabs to chat, inspect figures, and search semantically across the paper.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ─────────────────────────────────
    # TAB 1: CHAT
    # ─────────────────────────────────
    with tab_chat:
        if not st.session_state.messages:
            st.markdown("<span class='section-label'>Try these questions</span>",
                        unsafe_allow_html=True)
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
                    # Show saved matched figures
                    saved_figs = msg.get("matched_figures", [])
                    if saved_figs:
                        st.markdown(
                            "<div class='fig-match-banner'>📌 Related Figures from Paper</div>",
                            unsafe_allow_html=True
                        )
                        fig_cols = st.columns(len(saved_figs))
                        for col, fig in zip(fig_cols, saved_figs):
                            with col:
                                caption = f"{fig.fig_label}"
                                if fig.caption:
                                    caption += f" — {fig.caption}"
                                st.image(
                                    f"data:image/png;base64,{fig.image_base64}",
                                    caption=caption,
                                    width="stretch"
                                )
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
            render_question_turn(quick_question, active_id, paper_figures)
            st.rerun()

        # Chat input
        if prompt := st.chat_input("Ask anything about this paper..."):
            render_question_turn(prompt, active_id, paper_figures)

        if st.session_state.messages:
            if st.button("🗑 Clear Chat"):
                st.session_state.messages = []
                st.rerun()

    # ─────────────────────────────────
    # TAB 2: FIGURE GALLERY
    # ─────────────────────────────────
    with tab_figures:
        if not paper_figures:
            st.markdown("""
            <div style="text-align:center; padding:48px; color:var(--muted);">
                <div style="font-size:32px; margin-bottom:8px;">🖼</div>
                <div style="font-size:14px; color:var(--text);">No figures found in this paper.</div>
                <div style="font-size:12px; margin-top:6px; color:var(--soft);">
                    Some PDFs store images in formats that cannot be extracted.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div style='padding:8px 0 12px 0; font-size:13px; color:var(--muted);'>"
                f"{len(paper_figures)} figures extracted · Search or browse all</div>",
                unsafe_allow_html=True
            )

            display_figs = paper_figures

            for i in range(0, len(display_figs), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    if i + j < len(display_figs):
                        fig = display_figs[i + j]
                        with col:
                            with st.container():
                                st.markdown(f"""
                                <div class="fig-card">
                                    <div class="fig-label">{fig.fig_label} · Page {fig.page}</div>
                                    <div class="fig-caption">
                                        {fig.caption if fig.caption else "No caption detected"}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                st.image(
                                    f"data:image/png;base64,{fig.image_base64}",
                                    width="stretch"
                                )
                                st.markdown("<div style='height:8px'></div>",
                                            unsafe_allow_html=True)

    # ─────────────────────────────────
    # TAB 3: SEMANTIC SEARCH
    # ─────────────────────────────────
    with tab_search:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<span class='sec-label'>Search paper chunks by semantic similarity</span>",
                    unsafe_allow_html=True)

        search_col, k_col = st.columns([4, 1])
        with search_col:
            search_query = st.text_input(
                "Search Query",
                placeholder="e.g. attention mechanism, loss function, dataset...",
                label_visibility="collapsed"
            )
        with k_col:
            top_k = st.selectbox("Top K", [3, 5, 8, 10], index=1,
                                 label_visibility="collapsed")

        if search_query:
            with st.spinner("Searching..."):
                results = semantic_search(
                    query=search_query,
                    embedder=st.session_state.embedder,
                    index=st.session_state.index,
                    top_k=top_k,
                    filter_paper_id=active_id
                )

            st.markdown(f"<div style='font-size:12px; color:var(--muted); margin:10px 0;'>"
                        f"Found {len(results)} chunks</div>", unsafe_allow_html=True)

            for r in results:
                score_pct = int(r["score"] * 100)
                with st.expander(f"Chunk #{r['chunk_index']} — Score: {r['score']} ({score_pct}% match)"):
                    st.progress(r["score"])
                    st.markdown(f"""
                    <div class="source-chunk" style="max-height:300px; overflow-y:auto;">
                        {r['text']}
                    </div>""", unsafe_allow_html=True)

    # ─────────────────────────────────
    # TAB 4: RAG STATS
    # ─────────────────────────────────
    with tab_stats:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Papers Indexed", len(st.session_state.papers))
        c2.metric("Total Chunks", sum(p.get("chunk_count", 0)
                  for p in st.session_state.papers.values()))
        c3.metric("Vectors in Pinecone", sum(p.get("vectors_upserted", 0)
                  for p in st.session_state.papers.values()))
        c4.metric("Figures Extracted", sum(len(p.get("figures", []))
                  for p in st.session_state.papers.values()))

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown("<span class='section-label'>Architecture</span>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="panel" style="font-size:12px; color:var(--muted); line-height:2;">
            PDF Upload → PyMuPDF text + figure extraction<br/>
            → Chunk (500 words, 100 overlap)<br/>
            → sentence-transformers all-MiniLM-L6-v2 (384 dimensions)<br/>
            → Pinecone upsert (cosine similarity index)<br/>
            ────────────────────────────────────<br/>
            Query → embed → Pinecone top-K search<br/>
            → Retrieved chunks + keyword-matched figures<br/>
            → LLaMA 3.1 (Groq) → grounded answer + figures shown
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-bar">
    <div>Built by Sagar Kafle</div>
    <div>InsightPaper AI</div>
</div>
""", unsafe_allow_html=True)

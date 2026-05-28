# app.py — Research Paper Q&A Engine (RAG)
import json
import os

import streamlit as st
from dotenv import load_dotenv

from src.llm_qa import generate_paper_summary
from src.pdf_parser import parse_paper
from src.rag_pipeline import (chunk_text, make_paper_id, semantic_search,
                              upsert_paper)
from src.state import APP_STATE_FILE, DEFAULTS, load_app_state, save_app_state
from src.stream_helpers import init_clients, render_question_turn
from src.ui import (populate_tabs, render_css, render_dashboard, render_footer,
                    render_landing, render_navbar)

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

# CSS is provided by src.ui.css


# Initialize session defaults and load persisted state
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

load_app_state(st.session_state)


# ═══════════════════════════════════════════════════════
# NAVBAR
# ═══════════════════════════════════════════════════════
render_css()
render_navbar()


# ═══════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════
if not st.session_state.papers:
    render_landing()


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

    # render dashboard and get tab handles
    tab_chat, tab_figures, tab_search, tab_stats = render_dashboard()

    # populate the tabs UI (chat, figures, search, stats)
    from src.ui import populate_tabs
    populate_tabs(tab_chat, tab_figures, tab_search, tab_stats)

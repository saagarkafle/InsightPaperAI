import os

import streamlit as st
from dotenv import load_dotenv

from src.mvc import AppController, AppModel, AppView

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

controller = AppController(model=AppModel(), view=AppView())
controller.run()

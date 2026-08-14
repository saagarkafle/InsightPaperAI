from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st

# Sync Streamlit Cloud secrets to environment variables if deployed on Streamlit Cloud
for secret_key in ["PINECONE_API_KEY", "GROQ_API_KEY"]:
    if secret_key not in os.environ and secret_key in st.secrets:
        os.environ[secret_key] = st.secrets[secret_key]


from src.mvc import AppController, AppModel, AppView

st.set_page_config(
    page_title="InsightPaper AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

AppController(model=AppModel(), view=AppView()).run()

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from src.mvc import AppController, AppModel, AppView

st.set_page_config(
    page_title="InsightPaper AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

AppController(model=AppModel(), view=AppView()).run()

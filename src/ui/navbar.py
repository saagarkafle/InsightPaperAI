import streamlit as st


def render_navbar():
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

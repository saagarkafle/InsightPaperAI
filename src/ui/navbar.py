import streamlit as st


def render_navbar():
    st.markdown("""
<div class="topbar">
    <div class="brand">
        <a href="?home=1" style="text-decoration:none; color:inherit; display:flex; gap:12px; align-items:center;">
            <div class="brand-mark">I</div>
            <div>
                <div class="brand-title">InsightPaper AI</div>
                <div class="brand-subtitle">AI-Powered Research Paper Analysis</div>
            </div>
        </a>
    </div>
</div>
<div class="topbar-accent-line"></div>
""", unsafe_allow_html=True)

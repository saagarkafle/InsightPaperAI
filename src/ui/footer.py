import streamlit as st


def render_footer():
    st.markdown("""
    <div class="footer-bar">
        <div>Built by Sagar Kafle</div>
        <div>InsightPaper AI</div>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st


def render_css():
    st.markdown("""
<style>
/* condensed CSS file for UI package */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root { --bg:#121212; --panel:#181818; --panel-2:#202020; --line:#2f2f2f; --text:#f5f5f5; --muted:#b3b3b3; --soft:#9ca3af; --green:#1db954; --green-2:#169c46; --shadow:0 18px 50px rgba(0,0,0,0.38); }

html, body, .stApp { background: radial-gradient(circle at top left, rgba(29,185,84,0.12), transparent 26%), radial-gradient(circle at 90% 10%, rgba(29,185,84,0.08), transparent 20%), linear-gradient(180deg,#0f0f0f 0%,#111111 100%) !important; font-family: 'Inter', sans-serif !important; color: var(--text); }

.topbar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:18px 24px;margin:-1rem -1rem 20px -1rem;background:rgba(18,18,18,0.92);backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,0.06);position:sticky;top:0;z-index:100}

/* Other styles are similar to original app but trimmed for brevity; keep critical classes used in templates */
.chip{display:inline-flex;align-items:center;gap:6px;padding:8px 12px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.04);color:var(--muted);font-size:12px;font-weight:600}
.hero-card,.panel,.fig-card,.source-chunk{border:1px solid rgba(255,255,255,0.08)!important;background:linear-gradient(180deg,rgba(255,255,255,0.04),rgba(255,255,255,0.02))!important;border-radius:22px!important;box-shadow:var(--shadow)}
.panel{padding:22px}
.panel.compact{padding:16px}
.panel-title{font-size:12px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.panel-kicker{color:var(--green);font-size:12px;font-weight:700}
.sec-label{font-size:11px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:12px}
.fig-match-banner{background:rgba(29,185,84,0.12);border:1px solid rgba(29,185,84,0.2);border-radius:999px;padding:8px 14px;font-size:11px;font-weight:800;color:#dff7e6;letter-spacing:1px;text-transform:uppercase;margin:14px 0 10px 0}

/* Hide default Streamlit chrome */
#MainMenu, footer, .stDeployButton, [data-testid="stDeployButton"] { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar{width:8px} ::-webkit-scrollbar-track{background:#121212} ::-webkit-scrollbar-thumb{background:#3a3a3a;border-radius:999px}

</style>
""", unsafe_allow_html=True)

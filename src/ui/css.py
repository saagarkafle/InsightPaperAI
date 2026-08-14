import streamlit as st


def render_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    color-scheme: light !important;
    --bg: #DBEAFE;
    --bg-2: #EFF6FF;
    --bg-3: #E0EFFE;
    --panel: #EFF6FF;
    --line: #BFDBFE;
    --line-light: #93C5FD;
    --text: #0F172A;
    --text-secondary: #475569;
    --muted: #64748B;
    --soft: #94A3B8;
    --accent: #047857;
    --accent-light: rgba(4, 120, 87, 0.15);
    --accent-hover: #065F46;
    --green: #047857;
    --green-light: rgba(4, 120, 87, 0.15);
    --amber: #D97706;
    --amber-light: rgba(217, 119, 6, 0.15);
    --red: #DC2626;
    --red-light: rgba(220, 38, 38, 0.15);
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.08);
    --shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    --shadow-md: 0 6px 16px rgba(15, 23, 42, 0.16);
    --radius: 12px;
    --radius-sm: 8px;
    --radius-lg: 16px;
}

html,
body,
.stApp {
    color-scheme: light !important;
    background: #DBEAFE !important;
    color: #0F172A !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stBottom"],
.main {
    background: #DBEAFE !important;
    color: #0F172A !important;
}

[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 1280px;
}

/* ──────── HEADER BAR ──────── */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 14px 0;
    margin-bottom: 0;
    background: #DBEAFE;
    border-bottom: 1px solid #BFDBFE;
    position: relative;
    z-index: 10;
}

.topbar-accent-line {
    height: 3px;
    background: #047857;
    margin: 0 0 20px 0;
    border: none;
    border-radius: 0 0 2px 2px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: #047857 !important;
    color: #FFFFFF !important;
    display: grid;
    place-items: center;
    font-weight: 900;
    font-size: 18px;
}

.brand-title {
    font-weight: 900;
    font-size: 19px;
    line-height: 1;
    letter-spacing: -0.3px;
    color: #000000 !important;
}

.brand-subtitle {
    color: #000000 !important;
    font-size: 12px;
    margin-top: 3px;
    font-weight: 700;
}

/* ──────── CARDS & PANELS (Unified Card System) ──────── */
.card {
    background: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    padding: 22px !important;
    margin-bottom: 16px !important;
    color: #000000 !important;
}

.card-flat {
    background: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    padding: 18px !important;
    margin-bottom: 12px !important;
    color: #000000 !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease !important;
}

.card-flat:hover {
    border-color: #3B82F6 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.09) !important;
}

.card-accent {
    background: rgba(4, 120, 87, 0.08) !important;
    border: 1.5px solid #047857 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    padding: 18px !important;
    margin-bottom: 12px !important;
    color: #000000 !important;
}

/* ──────── UPLOAD CARDS ──────── */
.upload-card {
    border: 2px dashed #93C5FD !important;
    border-radius: 14px !important;
    padding: 24px 20px !important;
    text-align: center !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    margin-bottom: 16px !important;
    color: #000000 !important;
    transition: border-color 0.2s ease, background 0.2s ease, transform 0.18s ease !important;
}

.upload-card:hover {
    border-color: #0D9488 !important;
    background: rgba(13, 148, 136, 0.06) !important;
    transform: translateY(-2px);
}

.upload-card-icon {
    font-size: 32px;
    margin-bottom: 8px;
    display: block;
}

.upload-card-title {
    font-weight: 800 !important;
    font-size: 14px;
    color: #000000 !important;
    margin-bottom: 4px;
}

.upload-card-desc {
    font-size: 12px;
    color: #000000 !important;
    font-weight: 500;
    line-height: 1.5;
}

/* ──────── SECTION LABELS ──────── */
.section-label,
.sec-label,
.panel-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #000000 !important;
    margin-bottom: 12px;
    display: block;
    padding-bottom: 8px;
    border-bottom: 1.5px solid #BFDBFE;
}

.section-divider {
    height: 1px;
    background: #BFDBFE;
    margin: 20px 0;
    border: none;
}

/* ──────── HERO CARD ──────── */
.hero-card {
    background: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    padding: 26px !important;
    margin-bottom: 20px !important;
}

.panel-kicker {
    color: #047857 !important;
    font-size: 12px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.hero-title {
    font-size: clamp(24px, 2.5vw, 36px);
    line-height: 1.15;
    font-weight: 900;
    letter-spacing: -0.8px;
    margin-top: 8px;
    color: #000000 !important;
}

.hero-highlight {
    color: #047857 !important;
    font-weight: 900;
}

.hero-copy {
    margin-top: 12px;
    color: #000000 !important;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.7;
}

.hero-actions {
    margin-top: 16px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.hero-badge-row {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

/* ──────── CHIPS & TAGS ──────── */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid #BFDBFE;
    background: #E0EFFE;
    color: #475569;
    font-size: 12px;
    font-weight: 600;
}

.pill-tag {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(4, 120, 87, 0.4);
    background: rgba(4, 120, 87, 0.15);
    color: #047857;
    font-size: 11px;
    font-weight: 800;
}

.kw-tag {
    display: inline-flex;
    margin-right: 6px;
    margin-bottom: 6px;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(4, 120, 87, 0.4);
    background: rgba(4, 120, 87, 0.15);
    color: #047857;
    font-size: 11px;
    font-weight: 800;
}

/* ──────── PROGRESS BAR ──────── */
[data-testid="stProgress"] > div > div > div,
[data-testid="stProgress"] p,
[data-testid="stProgress"] span,
[data-testid="stProgress"] div {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* ──────── LIBRARY ITEMS / SIDEBAR CARDS ──────── */
.library-item {
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    margin-bottom: 8px !important;
    transition: border-color 0.15s ease, transform 0.15s ease !important;
}

.library-item:hover {
    border-color: #3B82F6 !important;
    transform: translateY(-1px);
}

.library-item.active {
    border-color: #047857 !important;
    background: rgba(4, 120, 87, 0.12) !important;
}

.library-label {
    color: #047857 !important;
    font-size: 11px;
    margin-bottom: 4px;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.library-title {
    font-weight: 900 !important;
    color: #000000 !important;
    line-height: 1.3;
    font-size: 14px;
}

.library-meta {
    color: #000000 !important;
    font-size: 12px;
    margin-top: 4px;
    font-weight: 500;
    line-height: 1.55;
}

/* ──────── STATS / METRIC PILLS ──────── */
.stat-grid-row {
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
    padding-bottom: 6px;
}

.stat-pill {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 12px 14px;
    border-radius: 14px;
    background: #EFF6FF;
    border: 1.5px solid #93C5FD;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.stat-pill .val {
    font-size: 18px;
    font-weight: 900;
    color: #000000;
}

.stat-pill .lbl {
    font-size: 11px;
    color: #000000;
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 800;
}

/* ──────── OVERVIEW GRID ──────── */
.overview-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 16px;
}

.overview-copy {
    color: #000000 !important;
    font-size: 14px;
    line-height: 1.7;
    font-weight: 500;
}

.findings-stack {
    display: grid;
    gap: 8px;
}

.finding-item {
    padding: 12px 14px;
    border-radius: 14px;
    border: 1.5px solid #93C5FD;
    background: #EFF6FF;
    color: #000000 !important;
    font-size: 13px;
    line-height: 1.55;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

/* ──────── DIFFICULTY BADGES ──────── */
.diff-beginner,
.diff-intermediate,
.diff-advanced {
    display: inline-flex;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.diff-beginner {
    background: rgba(29, 185, 84, 0.2);
    border: 1px solid rgba(29, 185, 84, 0.4);
    color: #1ED760;
}

.diff-intermediate {
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #FBBF24;
}

.diff-advanced {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #F87171;
}

/* ──────── FIGURES CARDS ──────── */
.fig-card {
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 14px !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    margin-bottom: 12px !important;
    color: #000000 !important;
}

.fig-label {
    color: #000000 !important;
    font-weight: 800;
    font-size: 14px;
}

.fig-caption {
    margin-top: 4px;
    color: #000000 !important;
    font-size: 13px;
    font-weight: 500;
}

.fig-match-banner {
    background: rgba(4, 120, 87, 0.12);
    border: 1.5px solid #047857;
    border-radius: 500px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 800;
    color: #047857;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin: 14px 0 10px 0;
}

/* ──────── SOURCE CHUNK CARDS ──────── */
.source-chunk {
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 16px !important;
    font-size: 13px !important;
    color: #000000 !important;
    line-height: 1.6 !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    margin-bottom: 10px !important;
}

.score-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid rgba(4, 120, 87, 0.4);
    background: rgba(4, 120, 87, 0.15);
    color: #047857;
    font-size: 11px;
    font-weight: 800;
}

.source-type-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid #93C5FD;
    background: #EFF6FF;
    color: #000000;
    font-size: 11px;
    font-weight: 700;
    margin-left: 6px;
}

/* ──────── SEARCH ──────── */
.search-results-scroll {
    max-height: min(60vh, 720px);
    overflow-y: auto;
    padding-right: 6px;
}

.search-results-scroll .stExpander {
    margin-bottom: 0.55rem;
}

.search-results-scroll .source-chunk {
    max-height: 260px;
    overflow-y: auto;
}

/* ──────── EVAL TABLE / ROW CARDS ──────── */
.eval-row {
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 16px !important;
    background: #EFF6FF !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    margin-bottom: 12px !important;
    color: #000000 !important;
}

.eval-question {
    font-weight: 800;
    font-size: 14px;
    color: #000000 !important;
    margin-bottom: 6px;
}

.eval-score {
    display: inline-flex;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 6px;
}

.eval-score-good {
    background: rgba(29, 185, 84, 0.2);
    color: #1ED760;
    border: 1px solid rgba(29, 185, 84, 0.4);
}

.eval-score-mid {
    background: rgba(245, 158, 11, 0.2);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.eval-score-low {
    background: rgba(239, 68, 68, 0.2);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

/* ──────── VERTICAL TABBAR ──────── */
.vertical-tabbar {
    padding: 6px 4px;
}
.vertical-tabbar .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.vertical-tabbar input[type="radio"] + label,
.vertical-tabbar [data-testid="stRadio"] label,
.vertical-tabbar [data-testid="stRadio"] div[role="radiogroup"] label {
    display: block;
    padding: 10px 14px;
    border-radius: 500px;
    border: 1px solid #BFDBFE;
    background: #EFF6FF;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
    font-size: 13px;
    transition: all 0.15s ease;
}
.vertical-tabbar [data-testid="stRadio"] label p,
.vertical-tabbar [data-testid="stRadio"] label span,
.vertical-tabbar [data-testid="stRadio"] label div,
.vertical-tabbar input[type="radio"] + label p,
.vertical-tabbar input[type="radio"] + label span,
.vertical-tabbar input[type="radio"] + label div {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
}
.vertical-tabbar input[type="radio"]:checked + label,
.vertical-tabbar [data-testid="stRadio"] label:has(input:checked) {
    background: #1DB954 !important;
    border-color: #1DB954 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
}
.vertical-tabbar input[type="radio"]:checked + label *,
.vertical-tabbar [data-testid="stRadio"] label:has(input:checked) * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
}

/* ──────── BUTTONS (Emerald Pill Tag Theme matching Pinecone/Groq/PyMuPDF badges) ──────── */
.stButton > button,
button[kind="primary"],
button[kind="secondary"],
div[data-testid="stButton"] > button {
    border-radius: 500px !important;
    border: 1.5px solid #047857 !important;
    background: rgba(4, 120, 87, 0.15) !important;
    background-color: rgba(4, 120, 87, 0.15) !important;
    color: #047857 !important;
    -webkit-text-fill-color: #047857 !important;
    font-weight: 800 !important;
    padding: 0.65rem 1.4rem !important;
    font-size: 14px !important;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(4, 120, 87, 0.12) !important;
    transition: all 0.15s ease !important;
}

.stButton > button p,
.stButton > button span,
.stButton > button div,
div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span,
div[data-testid="stButton"] > button div {
    color: #047857 !important;
    -webkit-text-fill-color: #047857 !important;
    font-weight: 800 !important;
}

.stButton > button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover,
div[data-testid="stButton"] > button:hover {
    background: rgba(4, 120, 87, 0.28) !important;
    background-color: rgba(4, 120, 87, 0.28) !important;
    color: #047857 !important;
    border: 1.5px solid #047857 !important;
    box-shadow: 0 4px 14px rgba(4, 120, 87, 0.25) !important;
    transform: scale(1.02);
}

.stButton > button:disabled,
div[data-testid="stButton"] > button:disabled {
    background: rgba(4, 120, 87, 0.08) !important;
    background-color: rgba(4, 120, 87, 0.08) !important;
    color: rgba(4, 120, 87, 0.6) !important;
    -webkit-text-fill-color: rgba(4, 120, 87, 0.6) !important;
    border: 1.5px solid rgba(4, 120, 87, 0.3) !important;
    opacity: 0.8 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

.stButton > button:disabled p,
.stButton > button:disabled span,
div[data-testid="stButton"] > button:disabled p,
div[data-testid="stButton"] > button:disabled span {
    color: rgba(4, 120, 87, 0.6) !important;
    -webkit-text-fill-color: rgba(4, 120, 87, 0.6) !important;
    font-weight: 800 !important;
}

/* ──────── SELECTBOX & DROPDOWN (Matches Emerald Pill Theme) ──────── */
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label,
[data-testid="stMultiSelect"] label {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* Outer select box shape */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] [data-baseweb="select"],
div[data-baseweb="select"] {
    background: transparent !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="select"] div[role="combobox"],
div[data-testid="stSelectbox"] div[role="combobox"] {
    background: rgba(4, 120, 87, 0.15) !important;
    background-color: rgba(4, 120, 87, 0.15) !important;
    border: 1.5px solid #047857 !important;
    border-radius: 500px !important;
    color: #047857 !important;
    -webkit-text-fill-color: #047857 !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 8px rgba(4, 120, 87, 0.12) !important;
    transition: all 0.15s ease !important;
    padding-left: 14px !important;
    padding-right: 14px !important;
    min-height: 42px !important;
    cursor: pointer !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:hover {
    background: rgba(4, 120, 87, 0.25) !important;
    background-color: rgba(4, 120, 87, 0.25) !important;
    border: 1.5px solid #047857 !important;
    box-shadow: 0 4px 14px rgba(4, 120, 87, 0.25) !important;
}

/* Inner elements inside the selectbox trigger */
div[data-testid="stSelectbox"] [data-baseweb="select"] div,
div[data-testid="stSelectbox"] [data-baseweb="select"] span,
div[data-testid="stSelectbox"] [data-baseweb="select"] p,
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] p,
div[data-testid="stSelectbox"] [aria-selected="true"] {
    color: #047857 !important;
    -webkit-text-fill-color: #047857 !important;
    font-weight: 800 !important;
    background: transparent !important;
    background-color: transparent !important;
}

div[data-testid="stSelectbox"] svg,
div[data-baseweb="select"] svg,
div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
    fill: #047857 !important;
    color: #047857 !important;
    stroke: #047857 !important;
}

/* Dropdown popover list styling */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
[data-baseweb="menu"] {
    background-color: #EFF6FF !important;
    background: #EFF6FF !important;
    border: 1.5px solid #3B82F6 !important;
    border-radius: 14px !important;
    color: #000000 !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.15) !important;
    overflow: hidden !important;
    padding: 4px !important;
}

li[role="option"],
ul[role="listbox"] li,
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"] {
    background-color: #EFF6FF !important;
    background: #EFF6FF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    margin: 2px 0 !important;
    transition: background-color 0.15s ease, color 0.15s ease !important;
    cursor: pointer !important;
}

li[role="option"] span,
li[role="option"] p,
li[role="option"] div,
ul[role="listbox"] li *,
[data-baseweb="menu"] li * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
}

/* Option Hover & Active State: Navy Blue (#1E3A8A) background + White text */
li[role="option"]:hover,
li[role="option"]:focus,
li[role="option"][aria-selected="true"],
li[role="option"][data-highlighted="true"],
ul[role="listbox"] li:hover,
ul[role="listbox"] li:focus,
ul[role="listbox"] li[aria-selected="true"],
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li:focus,
[data-baseweb="menu"] li[aria-selected="true"],
[data-baseweb="menu"] [aria-selected="true"] {
    background-color: #1E3A8A !important;
    background: #1E3A8A !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}

li[role="option"]:hover *,
li[role="option"]:focus *,
li[role="option"][aria-selected="true"] *,
li[role="option"][data-highlighted="true"] *,
ul[role="listbox"] li:hover *,
ul[role="listbox"] li:focus *,
ul[role="listbox"] li[aria-selected="true"] *,
[data-baseweb="menu"] li:hover *,
[data-baseweb="menu"] li:focus *,
[data-baseweb="menu"] li[aria-selected="true"] *,
[data-baseweb="menu"] [aria-selected="true"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* ──────── TABS ──────── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 6px;
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: 500px;
    border: 1px solid #BFDBFE;
    background: #EFF6FF;
    padding: 8px 16px;
    font-weight: 700;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-size: 13px;
}

[data-testid="stTabs"] [role="tab"] p,
[data-testid="stTabs"] [role="tab"] span,
[data-testid="stTabs"] [role="tab"] div {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    border-color: #1DB954 !important;
    background: #1DB954 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
}

[data-testid="stTabs"] [aria-selected="true"] p,
[data-testid="stTabs"] [aria-selected="true"] span,
[data-testid="stTabs"] [aria-selected="true"] div {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 800 !important;
}

/* ──────── FILE UPLOADER ──────── */
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stFileUploader"] {
    border-radius: 14px;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #DBEAFE !important;
    border: 2px dashed #93C5FD !important;
    border-radius: 14px !important;
    color: #000000 !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #0D9488 !important;
    background-color: rgba(13, 148, 136, 0.06) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div {
    color: #000000 !important;
    font-weight: 600;
}

/* Uploaded file preview row / tag */
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFileData"],
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] ul,
div[data-testid="stFileUploader"] li,
div.stFileUploader [data-testid="stFileUploaderFile"],
div.stFileUploader [data-testid="stFileUploaderFileData"] {
    background-color: #DBEAFE !important;
    background: #DBEAFE !important;
    border: 1.5px solid #3B82F6 !important;
    border-radius: 12px !important;
    color: #000000 !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
}

[data-testid="stFileUploaderFile"] *,
[data-testid="stFileUploaderFileData"] *,
[data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"] *,
div.stFileUploader [data-testid="stFileUploaderFile"] *,
div.stFileUploader [data-testid="stFileUploaderFileData"] * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 700 !important;
}

/* File icon container inside the pill */
div.stFileUploader [data-testid="stFileUploaderFile"] > div:first-child,
div.stFileUploader [data-testid="stFileUploaderFileData"] > div:first-child {
    background: #DBEAFE !important;
    border: 1px solid #93C5FD !important;
    border-radius: 8px !important;
}

/* Delete button ⓧ inside the pill */
div.stFileUploader [data-testid="stFileUploaderDeleteBtn"],
div.stFileUploader [data-testid="stFileUploaderDeleteBtn"] button,
div[data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"],
div[data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"] button,
[data-testid="stFileUploaderFile"] button,
[data-testid="stFileUploaderFileData"] button,
[data-testid="stFileUploader"] button {
    background-color: #DBEAFE !important;
    background: #DBEAFE !important;
    color: #000000 !important;
    border: 1px solid #93C5FD !important;
    border-radius: 50% !important;
}

div.stFileUploader [data-testid="stFileUploaderDeleteBtn"]:hover,
div.stFileUploader [data-testid="stFileUploaderDeleteBtn"] button:hover,
div[data-testid="stFileUploader"] [data-testid="stFileUploaderDeleteBtn"] button:hover,
[data-testid="stFileUploaderFile"] button:hover,
[data-testid="stFileUploaderFileData"] button:hover,
[data-testid="stFileUploader"] button:hover {
    background-color: #BFDBFE !important;
    background: #BFDBFE !important;
    border-color: #3B82F6 !important;
}

div.stFileUploader [data-testid="stFileUploaderDeleteBtn"] svg,
div.stFileUploader [data-testid="stFileUploaderDeleteBtn"] path,
[data-testid="stFileUploaderDeleteBtn"] * {
    color: #000000 !important;
    fill: #000000 !important;
    stroke: #000000 !important;
}

/* ──────── FOOTER ──────── */
.footer-bar {
    margin-top: 40px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid #93C5FD;
    color: #000000 !important;
    font-size: 13px;
    font-weight: 700;
}

.footer-bar div {
    color: #000000 !important;
    font-weight: 700;
}

/* ──────── METRIC CARDS ──────── */
[data-testid="stMetric"] {
    background: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
    min-width: 0 !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #000000 !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 4px !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.3 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #000000 !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    word-break: break-word !important;
}

/* Chat Message specific metrics override */
[data-testid="stChatMessage"] [data-testid="stMetric"] {
    padding: 4px 8px !important;
}

[data-testid="stChatMessage"] [data-testid="stMetricLabel"],
[data-testid="stChatMessage"] [data-testid="stMetricLabel"] * {
    font-size: 9px !important;
    margin-bottom: 2px !important;
    line-height: 1.1 !important;
}

[data-testid="stChatMessage"] [data-testid="stMetricValue"],
[data-testid="stChatMessage"] [data-testid="stMetricValue"] * {
    font-size: 12px !important;
}

/* ──────── CHAT MESSAGES & BUBBLES ──────── */
[data-testid="stChatMessage"],
.stChatMessage {
    background-color: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    margin-bottom: 12px !important;
    color: #000000 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background-color: #EFF6FF !important;
    border-color: #0D9488 !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: #EFF6FF !important;
    border-color: #93C5FD !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
}

[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] *,
.stChatMessageContent,
.stChatMessageContent * {
    color: #000000 !important;
    font-weight: 500;
}

[data-testid="stChatMessageContent"] pre,
[data-testid="stChatMessageContent"] code {
    background-color: #DBEAFE !important;
    color: #047857 !important;
    font-weight: 700;
    border-radius: 6px;
}

/* ──────── EXPANDERS ──────── */
[data-testid="stExpander"] {
    background-color: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* ──────── SELECTBOX & INPUT OVERRIDES ──────── */
/* Cleanly handled in global selectbox rule above */

/* ──────── HIDE STREAMLIT DEFAULTS ──────── */
#MainMenu,
footer,
.stDeployButton,
[data-testid="stDeployButton"] {
    display: none !important;
}

/* ──────── SCROLLBAR ──────── */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #DBEAFE;
}

::-webkit-scrollbar-thumb {
    background: #93C5FD;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #60A5FA;
}

/* ──────── RESPONSIVE ──────── */
@media (max-width: 1024px) {
    .overview-grid {
        grid-template-columns: 1fr;
    }

    .topbar {
        position: static;
    }
}

@media (max-width: 760px) {
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .topbar {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        margin-left: 0;
        margin-right: 0;
    }

    .hero-card,
    .card,
    .card-flat {
        border-radius: var(--radius) !important;
    }

    .footer-bar {
        width: calc(100% - 1rem);
        left: 50%;
        bottom: 8px;
        flex-direction: column;
        gap: 4px;
        text-align: center;
    }
}

</style>
""", unsafe_allow_html=True)

import streamlit as st


def render_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    color-scheme: dark !important;
    --bg: #121212;
    --bg-2: #181818;
    --bg-3: #242424;
    --panel: #181818;
    --line: #282828;
    --line-light: #333333;
    --text: #FFFFFF;
    --text-secondary: #B3B3B3;
    --muted: #A7A7A7;
    --soft: #727272;
    --accent: #1DB954;
    --accent-light: rgba(29, 185, 84, 0.15);
    --accent-hover: #1ED760;
    --green: #1DB954;
    --green-light: rgba(29, 185, 84, 0.15);
    --amber: #F59E0B;
    --amber-light: rgba(245, 158, 11, 0.15);
    --red: #EF4444;
    --red-light: rgba(239, 68, 68, 0.15);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.5);
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
    --shadow-md: 0 6px 16px rgba(0, 0, 0, 0.7);
    --radius: 12px;
    --radius-sm: 8px;
    --radius-lg: 16px;
}

html,
body,
.stApp {
    color-scheme: dark !important;
    background: #121212 !important;
    color: #FFFFFF !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stBottom"],
.main {
    background: #121212 !important;
    color: #FFFFFF !important;
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
    background: #121212;
    border-bottom: 1px solid #282828;
    position: relative;
    z-index: 10;
}

.topbar-accent-line {
    height: 3px;
    background: #1DB954;
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
    background: #1DB954 !important;
    color: #000000 !important;
    display: grid;
    place-items: center;
    font-weight: 900;
    font-size: 18px;
}

.brand-title {
    font-weight: 800;
    font-size: 18px;
    line-height: 1;
    letter-spacing: -0.3px;
    color: #FFFFFF !important;
}

.brand-subtitle {
    color: #B3B3B3 !important;
    font-size: 12px;
    margin-top: 3px;
    font-weight: 500;
}

/* ──────── CARDS & PANELS ──────── */
.card {
    background: #181818;
    border: 1px solid #282828;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    margin-bottom: 16px;
}

.card-flat {
    background: #242424;
    border: 1px solid #333333;
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 12px;
}

.card-accent {
    background: rgba(29, 185, 84, 0.12);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 12px;
}

/* ──────── UPLOAD CARDS ──────── */
.upload-card {
    border: 2px dashed #333333;
    border-radius: var(--radius);
    padding: 24px 20px;
    text-align: center;
    background: #181818;
    margin-bottom: 16px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.upload-card:hover {
    border-color: #1DB954;
    background: rgba(29, 185, 84, 0.08);
}

.upload-card-icon {
    font-size: 32px;
    margin-bottom: 8px;
    display: block;
}

.upload-card-title {
    font-weight: 700;
    font-size: 14px;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.upload-card-desc {
    font-size: 12px;
    color: #A7A7A7;
    line-height: 1.5;
}

/* ──────── SECTION LABELS ──────── */
.section-label,
.sec-label,
.panel-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #A7A7A7;
    margin-bottom: 12px;
    display: block;
    padding-bottom: 8px;
    border-bottom: 1px solid #282828;
}

.section-divider {
    height: 1px;
    background: #282828;
    margin: 20px 0;
    border: none;
}

/* ──────── HERO ──────── */
.hero-card {
    background: #181818;
    border: 1px solid #282828;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    padding: 28px;
    margin-bottom: 20px;
}

.panel-kicker {
    color: #1DB954;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.hero-title {
    font-size: clamp(24px, 2.5vw, 36px);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin-top: 8px;
    color: #FFFFFF;
}

.hero-highlight {
    color: #1DB954;
}

.hero-copy {
    margin-top: 12px;
    color: #B3B3B3;
    font-size: 14px;
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
    border: 1px solid #333333;
    background: #242424;
    color: #B3B3B3;
    font-size: 12px;
    font-weight: 600;
}

.pill-tag {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(29, 185, 84, 0.3);
    background: rgba(29, 185, 84, 0.15);
    color: #1ED760;
    font-size: 11px;
    font-weight: 700;
}

.kw-tag {
    display: inline-flex;
    margin-right: 6px;
    margin-bottom: 6px;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(245, 158, 11, 0.3);
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    font-size: 11px;
    font-weight: 700;
}

/* ──────── LIBRARY ITEMS ──────── */
.library-item {
    border: 1px solid #282828;
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    background: #181818;
    margin-bottom: 8px;
    transition: border-color 0.15s ease;
}

.library-item.active {
    border-color: #1DB954;
    background: rgba(29, 185, 84, 0.15);
}

.library-label {
    color: #727272;
    font-size: 11px;
    margin-bottom: 3px;
    font-weight: 600;
}

.library-title {
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
    font-size: 14px;
}

.library-meta {
    color: #A7A7A7;
    font-size: 12px;
    margin-top: 2px;
}

/* ──────── STATS ──────── */
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
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    background: #242424;
    border: 1px solid #333333;
}

.stat-pill .val {
    font-size: 18px;
    font-weight: 800;
    color: #FFFFFF;
}

.stat-pill .lbl {
    font-size: 10px;
    color: #A7A7A7;
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
}

/* ──────── OVERVIEW GRID ──────── */
.overview-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 16px;
}

.overview-copy {
    color: #B3B3B3;
    font-size: 15px;
    line-height: 1.75;
}

.findings-stack {
    display: grid;
    gap: 8px;
}

.finding-item {
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid #333333;
    background: #242424;
    color: #B3B3B3;
    font-size: 13px;
    line-height: 1.5;
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

/* ──────── FIGURES ──────── */
.fig-card {
    border: 1px solid #282828;
    border-radius: var(--radius);
    padding: 12px;
    background: #181818;
    box-shadow: var(--shadow-sm);
    margin-bottom: 8px;
}

.fig-label {
    color: #FFFFFF;
    font-weight: 700;
    font-size: 13px;
}

.fig-caption {
    margin-top: 4px;
    color: #A7A7A7;
    font-size: 12px;
}

.fig-match-banner {
    background: rgba(29, 185, 84, 0.15);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 700;
    color: #1ED760;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin: 14px 0 10px 0;
}

/* ──────── SOURCE CHUNKS ──────── */
.source-chunk {
    border: 1px solid #282828;
    border-radius: var(--radius-sm);
    padding: 14px;
    font-size: 13px;
    color: #B3B3B3;
    line-height: 1.6;
    background: #242424;
    margin-bottom: 8px;
}

.score-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid rgba(29, 185, 84, 0.4);
    background: rgba(29, 185, 84, 0.15);
    color: #1ED760;
    font-size: 11px;
    font-weight: 700;
}

.source-type-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid #333333;
    background: #242424;
    color: #A7A7A7;
    font-size: 11px;
    font-weight: 600;
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

/* ──────── EVAL TABLE ──────── */
.eval-row {
    border: 1px solid #282828;
    border-radius: var(--radius-sm);
    padding: 14px;
    background: #181818;
    margin-bottom: 10px;
}

.eval-question {
    font-weight: 700;
    font-size: 14px;
    color: #FFFFFF;
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
.vertical-tabbar input[type="radio"] + label {
    display: block;
    padding: 10px 14px;
    border-radius: 500px;
    border: 1px solid #282828;
    background: #181818;
    color: #B3B3B3;
    font-weight: 600;
    font-size: 13px;
    transition: all 0.15s ease;
}
.vertical-tabbar input[type="radio"]:checked + label {
    background: #1DB954 !important;
    border-color: #1DB954 !important;
    color: #000000 !important;
    font-weight: 800 !important;
}

/* ──────── BUTTONS (Spotify Pill Button) ──────── */
.stButton > button {
    border-radius: 500px !important;
    border: none !important;
    background: #1DB954 !important;
    color: #000000 !important;
    font-weight: 800 !important;
    padding: 0.6rem 1.4rem !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background: #1ED760 !important;
    color: #000000 !important;
    box-shadow: 0 4px 14px rgba(29, 185, 84, 0.4) !important;
    transform: scale(1.02);
}

.stButton > button:disabled {
    background: #282828 !important;
    color: #555555 !important;
    border: 1px solid #333333 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ──────── TABS ──────── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 6px;
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: 500px;
    border: 1px solid #282828;
    background: #181818;
    padding: 8px 16px;
    font-weight: 600;
    color: #B3B3B3;
    font-size: 13px;
}

[data-testid="stTabs"] [aria-selected="true"] {
    border-color: #1DB954;
    background: #1DB954;
    color: #000000;
    font-weight: 800;
}

/* ──────── FILE UPLOADER ──────── */
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stFileUploader"] {
    border-radius: var(--radius-sm);
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #181818 !important;
    border: 2px dashed #333333 !important;
    border-radius: var(--radius-sm) !important;
    color: #B3B3B3 !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #1DB954 !important;
    background-color: rgba(29, 185, 84, 0.08) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div {
    color: #B3B3B3 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 500px !important;
}

/* ──────── FOOTER ──────── */
.footer-bar {
    margin-top: 40px;
    padding: 12px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #282828;
    color: #A7A7A7;
    font-size: 12px;
}

/* ──────── METRICS ──────── */
[data-testid="stMetric"] {
    background: #181818 !important;
    border: 1px solid #282828 !important;
    border-radius: var(--radius-sm);
    padding: 10px 14px !important;
    min-width: 0 !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #A7A7A7 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.3 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #FFFFFF !important;
    font-size: 20px !important;
    font-weight: 700 !important;
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
    background-color: #181818 !important;
    border: 1px solid #282828 !important;
    border-radius: var(--radius) !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
    color: #FFFFFF !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background-color: #1C2921 !important;
    border-color: rgba(29, 185, 84, 0.35) !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: #181818 !important;
    border-color: #282828 !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] *,
.stChatMessageContent,
.stChatMessageContent * {
    color: #FFFFFF !important;
}

[data-testid="stChatMessageContent"] pre,
[data-testid="stChatMessageContent"] code {
    background-color: #121212 !important;
    color: #1ED760 !important;
    border-radius: 6px;
}

/* ──────── CHAT INPUT ──────── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background-color: #242424 !important;
    border-radius: 500px !important;
    border: 1px solid #383838 !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    color: #FFFFFF !important;
    background-color: #242424 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8E8E8E !important;
}

/* ──────── EXPANDERS ──────── */
[data-testid="stExpander"] {
    background-color: #181818 !important;
    border: 1px solid #282828 !important;
    border-radius: var(--radius-sm) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #FFFFFF !important;
}

/* ──────── SELECTBOX & INPUT OVERRIDES ──────── */
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] label,
[data-testid="stMultiSelect"] label {
    color: #B3B3B3 !important;
}

div[data-baseweb="select"] > div {
    background-color: #242424 !important;
    border-color: #383838 !important;
    color: #FFFFFF !important;
    border-radius: var(--radius-sm) !important;
}

div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

div[data-baseweb="popover"],
ul[role="listbox"] {
    background-color: #242424 !important;
    border: 1px solid #383838 !important;
    color: #FFFFFF !important;
}

li[role="option"] {
    background-color: #242424 !important;
    color: #FFFFFF !important;
}

li[role="option"]:hover {
    background-color: #2E2E2E !important;
}

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
    background: #121212;
}

::-webkit-scrollbar-thumb {
    background: #282828;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #383838;
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

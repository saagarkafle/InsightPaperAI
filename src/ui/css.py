import streamlit as st


def render_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: light !important;
    --bg: #FFFFFF;
    --bg-2: #F5F5F5;
    --bg-3: #FAFAFA;
    --panel: #FFFFFF;
    --line: #E5E7EB;
    --line-light: #F0F0F0;
    --text: #1A1A2E;
    --text-secondary: #374151;
    --muted: #6B7280;
    --soft: #9CA3AF;
    --accent: #4F8EF7;
    --accent-light: #EBF2FE;
    --accent-hover: #3B7AE8;
    --green: #10B981;
    --green-light: #ECFDF5;
    --amber: #F59E0B;
    --amber-light: #FFFBEB;
    --red: #EF4444;
    --red-light: #FEF2F2;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.06), 0 2px 4px rgba(0, 0, 0, 0.04);
    --radius: 12px;
    --radius-sm: 8px;
    --radius-lg: 16px;
}

html,
body,
.stApp {
    color-scheme: light !important;
    background: #FFFFFF !important;
    color: #1A1A2E !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stBottom"],
.main {
    background: #FFFFFF !important;
    color: #1A1A2E !important;
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
    background: var(--bg);
    border-bottom: 1px solid var(--line);
    position: relative;
    z-index: 10;
}

.topbar-accent-line {
    height: 3px;
    background: var(--accent);
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
    background: #4F8EF7 !important;
    color: #FFFFFF !important;
    display: grid;
    place-items: center;
    font-weight: 800;
    font-size: 18px;
}

.brand-title {
    font-weight: 800;
    font-size: 18px;
    line-height: 1;
    letter-spacing: -0.3px;
    color: #1A1A2E !important;
}

.brand-subtitle {
    color: #6B7280 !important;
    font-size: 12px;
    margin-top: 3px;
    font-weight: 500;
}

/* ──────── CARDS & PANELS ──────── */
.card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    margin-bottom: 16px;
}

.card-flat {
    background: var(--bg-2);
    border: 1px solid var(--line-light);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 12px;
}

.card-accent {
    background: var(--accent-light);
    border: 1px solid rgba(79, 142, 247, 0.2);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 12px;
}

/* ──────── UPLOAD CARDS ──────── */
.upload-card {
    border: 2px dashed var(--line);
    border-radius: var(--radius);
    padding: 24px 20px;
    text-align: center;
    background: var(--bg-3);
    margin-bottom: 16px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.upload-card:hover {
    border-color: var(--accent);
    background: var(--accent-light);
}

.upload-card-icon {
    font-size: 32px;
    margin-bottom: 8px;
    display: block;
}

.upload-card-title {
    font-weight: 700;
    font-size: 14px;
    color: var(--text);
    margin-bottom: 4px;
}

.upload-card-desc {
    font-size: 12px;
    color: var(--muted);
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
    color: var(--muted);
    margin-bottom: 12px;
    display: block;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--line-light);
}


.section-divider {
    height: 1px;
    background: var(--line-light);
    margin: 20px 0;
    border: none;
}

/* ──────── HERO ──────── */
.hero-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    padding: 28px;
    margin-bottom: 20px;
}

.panel-kicker {
    color: var(--accent);
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
    color: var(--text);
}

.hero-highlight {
    color: var(--accent);
}

.hero-copy {
    margin-top: 12px;
    color: var(--muted);
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
    border: 1px solid var(--line);
    background: var(--bg-2);
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
}

.pill-tag {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(79, 142, 247, 0.25);
    background: var(--accent-light);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
}

.kw-tag {
    display: inline-flex;
    margin-right: 6px;
    margin-bottom: 6px;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid rgba(245, 158, 11, 0.25);
    background: var(--amber-light);
    color: #92400E;
    font-size: 11px;
    font-weight: 700;
}

/* ──────── LIBRARY ITEMS ──────── */
.library-item {
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    background: var(--bg);
    margin-bottom: 8px;
    transition: border-color 0.15s ease;
}

.library-item.active {
    border-color: var(--accent);
    background: var(--accent-light);
}

.library-label {
    color: var(--soft);
    font-size: 11px;
    margin-bottom: 3px;
    font-weight: 600;
}

.library-title {
    font-weight: 700;
    color: var(--text);
    line-height: 1.3;
    font-size: 14px;
}

.library-meta {
    color: var(--muted);
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
    background: var(--bg-2);
    border: 1px solid var(--line-light);
}

.stat-pill .val {
    font-size: 18px;
    font-weight: 800;
    color: var(--text);
}

.stat-pill .lbl {
    font-size: 10px;
    color: var(--muted);
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
    color: var(--text-secondary);
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
    border: 1px solid var(--line-light);
    background: var(--bg-2);
    color: var(--text-secondary);
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
    background: var(--green-light);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #065F46;
}

.diff-intermediate {
    background: var(--amber-light);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #92400E;
}

.diff-advanced {
    background: var(--red-light);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #991B1B;
}

/* ──────── FIGURES ──────── */
.fig-card {
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 12px;
    background: var(--panel);
    box-shadow: var(--shadow-sm);
    margin-bottom: 8px;
}

.fig-label {
    color: var(--text);
    font-weight: 700;
    font-size: 13px;
}

.fig-caption {
    margin-top: 4px;
    color: var(--muted);
    font-size: 12px;
}

.fig-match-banner {
    background: var(--accent-light);
    border: 1px solid rgba(79, 142, 247, 0.25);
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin: 14px 0 10px 0;
}

/* ──────── SOURCE CHUNKS ──────── */
.source-chunk {
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    padding: 14px;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    background: var(--bg-2);
    margin-bottom: 8px;
}

.score-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid rgba(79, 142, 247, 0.3);
    background: var(--accent-light);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
}

.source-type-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: var(--bg-2);
    color: var(--muted);
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
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    padding: 14px;
    background: var(--panel);
    margin-bottom: 10px;
}

.eval-question {
    font-weight: 700;
    font-size: 14px;
    color: var(--text);
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
    background: var(--green-light);
    color: #065F46;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.eval-score-mid {
    background: var(--amber-light);
    color: #92400E;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.eval-score-low {
    background: var(--red-light);
    color: #991B1B;
    border: 1px solid rgba(239, 68, 68, 0.3);
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
    padding: 10px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--line);
    background: var(--bg);
    color: var(--muted);
    font-weight: 600;
    font-size: 13px;
    transition: all 0.15s ease;
}
.vertical-tabbar input[type="radio"]:checked + label {
    background: var(--accent-light);
    border-color: var(--accent);
    color: var(--accent);
}

/* ──────── BUTTONS ──────── */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--accent) !important;
    background: var(--accent) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 0.5rem 1rem !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background: var(--accent-hover) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px);
}

/* ──────── TABS ──────── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: var(--radius-sm);
    border: 1px solid var(--line);
    background: var(--bg);
    padding: 8px 14px;
    font-weight: 600;
    color: var(--muted);
    font-size: 13px;
}

[data-testid="stTabs"] [aria-selected="true"] {
    border-color: var(--accent);
    background: var(--accent-light);
    color: var(--accent);
}

/* ──────── FILE UPLOADER ──────── */
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stFileUploader"] {
    border-radius: var(--radius-sm);
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFFFF !important;
    border: 2px dashed #D1D5DB !important;
    border-radius: var(--radius-sm) !important;
    color: #374151 !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #4F8EF7 !important;
    background-color: #EBF2FE !important;
}

[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div {
    color: #374151 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #D1D5DB !important;
}

/* ──────── FOOTER ──────── */
.footer-bar {
    margin-top: 40px;
    padding: 12px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 12px;
}

/* ──────── METRICS ──────── */
[data-testid="stMetric"] {
    background: var(--bg-2);
    border: 1px solid var(--line-light);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 700 !important;
}

/* ──────── CHAT INPUT ──────── */
[data-testid="stChatInput"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--line) !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
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
    background: var(--bg-2);
}

::-webkit-scrollbar-thumb {
    background: var(--line);
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--soft);
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

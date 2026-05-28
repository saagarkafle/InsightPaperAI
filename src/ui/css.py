import streamlit as st


def render_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0d1310;
    --bg-2: #0f1713;
    --panel: #111d17;
    --panel-2: #15251d;
    --line: rgba(255, 255, 255, 0.09);
    --text: #ebf5ef;
    --muted: #9fb4a8;
    --soft: #7f988c;
    --green: #2ccf73;
    --green-2: #1ba85a;
    --gold: #d8bf72;
    --shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
}

html,
body,
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(44, 207, 115, 0.17), transparent 32%),
        radial-gradient(circle at 92% 8%, rgba(216, 191, 114, 0.14), transparent 22%),
        linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%) !important;
    color: var(--text);
    font-family: 'Manrope', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 1.1rem;
    padding-bottom: 1rem;
    max-width: 1260px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 16px 20px;
    margin: -0.5rem -0.6rem 18px -0.6rem;
    background: rgba(14, 23, 18, 0.82);
    border: 1px solid var(--line);
    border-radius: 18px;
    backdrop-filter: blur(8px);
    box-shadow: var(--shadow);
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--green), #74ecad);
    color: #042911;
    display: grid;
    place-items: center;
    font-weight: 900;
}

.brand-title {
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.2px;
}

.brand-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 11px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.03);
    color: var(--muted);
    font-size: 12px;
    font-weight: 700;
}

.hero-card,
.panel,
.stat-panel,
.fig-card,
.source-chunk,
.card-glow,
.stat-card {
    border: 1px solid var(--line) !important;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)) !important;
    border-radius: 18px !important;
    box-shadow: var(--shadow);
}

.hero-card {
    padding: 22px;
}

.hero-title {
    font-size: clamp(26px, 2.8vw, 42px);
    line-height: 1.08;
    font-weight: 900;
    letter-spacing: -1.1px;
    margin-top: 8px;
}

.hero-highlight {
    color: var(--gold);
}

.hero-copy {
    margin-top: 12px;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
}

.hero-actions,
.hero-badge-row {
    margin-top: 14px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.pill-tag {
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(44, 207, 115, 0.11);
    color: #d8fbe8;
    font-size: 11px;
    font-weight: 700;
}

.panel {
    padding: 20px;
}

.panel.compact {
    padding: 14px;
}

.panel-title,
.section-label,
.sec-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
    display: block;
}

.panel-kicker {
    color: var(--green);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.panel-copy,
.upload-note,
.library-meta,
.stat-note {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}

.library-item {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 10px 11px;
    background: rgba(255, 255, 255, 0.02);
    margin-bottom: 8px;
}

.library-item.active {
    border-color: rgba(44, 207, 115, 0.35);
    background: rgba(44, 207, 115, 0.08);
}

.library-label {
    color: var(--soft);
    font-size: 11px;
    margin-bottom: 3px;
}

.library-title {
    font-weight: 700;
    color: var(--text);
    line-height: 1.3;
    font-size: 14px;
}

.stat-panel {
    padding: 14px;
    min-height: 108px;
}

.stat-card {
    padding: 12px;
    text-align: center;
}

.stat-value {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -0.5px;
}

.stat-label {
    margin-top: 3px;
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.overview-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 14px;
}

.card-glow {
    background: linear-gradient(180deg, rgba(44, 207, 115, 0.12), rgba(255, 255, 255, 0.02)) !important;
}

.overview-copy {
    color: #d7e6dc;
    font-size: 15px;
    line-height: 1.75;
}

.findings-stack {
    display: grid;
    gap: 8px;
}

.finding-item {
    padding: 8px 10px;
    border-radius: 10px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.03);
    color: var(--text);
    font-size: 13px;
}

.kw-tag {
    display: inline-flex;
    margin-right: 7px;
    margin-bottom: 7px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(216, 191, 114, 0.14);
    color: #f3e6bf;
    font-size: 11px;
    font-weight: 700;
}

.diff-beginner,
.diff-intermediate,
.diff-advanced {
    display: inline-flex;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.diff-beginner {
    background: rgba(44, 207, 115, 0.16);
    border: 1px solid rgba(44, 207, 115, 0.36);
    color: #d9f8e7;
}

.diff-intermediate {
    background: rgba(216, 191, 114, 0.16);
    border: 1px solid rgba(216, 191, 114, 0.36);
    color: #f5e9c7;
}

.diff-advanced {
    background: rgba(240, 120, 120, 0.16);
    border: 1px solid rgba(240, 120, 120, 0.35);
    color: #ffdede;
}

.fig-card {
    padding: 10px;
    margin-bottom: 8px;
}

.fig-label {
    color: var(--text);
    font-weight: 800;
    font-size: 13px;
}

.fig-caption {
    margin-top: 4px;
    color: var(--muted);
    font-size: 12px;
}

.fig-match-banner {
    background: rgba(44, 207, 115, 0.15);
    border: 1px solid rgba(44, 207, 115, 0.3);
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 800;
    color: #def8e9;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 14px 0 10px 0;
}

.source-chunk {
    padding: 12px;
    font-size: 13px;
    color: #daebe0;
    line-height: 1.6;
}

.score-badge {
    display: inline-flex;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid rgba(44, 207, 115, 0.35);
    background: rgba(44, 207, 115, 0.16);
    color: #ddf9e9;
    font-size: 11px;
    font-weight: 700;
}

.footer-bar {
    margin-top: 20px;
    padding: 10px 4px 2px 4px;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--line);
    color: var(--soft);
    font-size: 12px;
}

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid var(--line) !important;
    background: linear-gradient(180deg, rgba(44, 207, 115, 0.16), rgba(44, 207, 115, 0.08)) !important;
    color: #ebfff4 !important;
    font-weight: 800 !important;
    padding: 0.55rem 0.95rem !important;
}

.stButton > button:hover {
    border-color: rgba(44, 207, 115, 0.48) !important;
    transform: translateY(-1px);
}

/* Keep a single upload limit line in the card and hide Streamlit's duplicate note. */
[data-testid="stFileUploaderDropzoneInstructions"] small {
    display: none !important;
}

[data-testid="stTabs"] [role="tablist"] {
    gap: 6px;
}

[data-testid="stTabs"] [role="tab"] {
    border-radius: 12px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.03);
    padding: 8px 14px;
}

[data-testid="stTabs"] [aria-selected="true"] {
    border-color: rgba(44, 207, 115, 0.44);
    background: rgba(44, 207, 115, 0.14);
}

#MainMenu,
footer,
.stDeployButton,
[data-testid="stDeployButton"] {
    display: none !important;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0d1310;
}

::-webkit-scrollbar-thumb {
    background: #2f473c;
    border-radius: 999px;
}

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
        gap: 12px;
        margin-left: 0;
        margin-right: 0;
    }

    .hero-card,
    .panel,
    .panel.compact,
    .stat-panel,
    .stat-card {
        border-radius: 14px !important;
    }

    .footer-bar {
        flex-direction: column;
        gap: 4px;
    }
}

</style>
""", unsafe_allow_html=True)

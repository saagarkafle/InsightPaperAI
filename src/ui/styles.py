# src/ui/styles.py
# CSS string constant injected at app startup to enforce a minimal, flat UI.

FLAT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Base typography and layout */
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #FFFFFF !important;
    color: #111827 !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}

/* Remove Streamlit default top colored bar and replace with blue (#4F8EF7) */
[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
    border-top: 4px solid #4F8EF7 !important;
}

/* Remove shadows, borders, and rounded corners from all elements */
* {
    box-shadow: none !important;
    border-radius: 0 !important;
}

/* Specific overrides for containers and interactive elements */
[data-testid="stChatInput"],
[data-testid="stFileUploader"],
[data-testid="stDataFrame"],
.stButton > button,
.stTextArea > div > div > textarea,
.stTextInput > div > div > input {
    border: 1px solid #E5E7EB !important;
    background-color: #FFFFFF !important;
}

/* Remove hover effects and shadows from buttons */
.stButton > button:hover {
    background-color: #F9FAFB !important;
    border-color: #D1D5DB !important;
    color: #111827 !important;
}

/* Remove default padding/margin in main container to make it flatter */
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    max-width: 900px !important;
}

/* Divider styling */
hr {
    margin: 1.5rem 0 !important;
    border-top: 1px solid #E5E7EB !important;
}

/* Hide deploy button, main menu, footer */
#MainMenu, footer, .stDeployButton, [data-testid="stDeployButton"] {
    display: none !important;
}

/* Make tabs completely flat */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #E5E7EB !important;
    gap: 20px;
}

[data-testid="stTabs"] [role="tab"] {
    border: none !important;
    background: transparent !important;
    padding: 10px 0 !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: #111827 !important;
    border-bottom: 2px solid #111827 !important;
}

/* Force metrics to be flat */
[data-testid="stMetric"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #6B7280 !important;
}
</style>
"""

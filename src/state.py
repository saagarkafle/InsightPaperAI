import json
import os
from dataclasses import asdict

from src.pdf_parser import Figure

# Default Streamlit session state
DEFAULTS = {
    "papers": {},
    "active_paper_id": None,
    "messages": [],
    "embedder": None,
    "index": None,
    "groq_client": None,
    "processing": False,
    "initialized": False,
    # Dataset state
    "dataset": None,
    "dataset_filename": None,
    "dataset_id": None,
    "source_mode": "both",  # "pdf", "dataset", or "both"
    "eval_results": None,
    # LLM model selection
    "selected_model": None,  # display name; resolved to model ID at call time
}


# App state file (project root)
APP_STATE_FILE = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), ".insightpaper_state.json")


def _serialize_papers(papers: dict) -> dict:
    serialized = {}
    for paper_id, paper in papers.items():
        paper_copy = dict(paper)
        paper_copy["figures"] = [
            asdict(fig) if hasattr(fig, "fig_label") else fig
            for fig in paper_copy.get("figures", [])
        ]
        serialized[paper_id] = paper_copy
    return serialized


def _deserialize_papers(papers: dict) -> dict:
    restored = {}
    for paper_id, paper in papers.items():
        paper_copy = dict(paper)
        paper_copy["figures"] = [
            Figure(**fig) if isinstance(fig, dict) else fig
            for fig in paper_copy.get("figures", [])
        ]
        restored[paper_id] = paper_copy
    return restored


def save_app_state(st_session_state) -> None:
    """No-op: App state is kept in per-user Streamlit session memory to prevent multi-user session state leaking."""
    pass


def load_app_state(st_session_state) -> None:
    """No-op: App state is kept in per-user Streamlit session memory to prevent multi-user session state leaking."""
    pass

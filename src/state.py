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
    payload = {
        "papers": _serialize_papers(st_session_state.papers),
        "active_paper_id": st_session_state.active_paper_id,
        "dataset_filename": st_session_state.get("dataset_filename"),
        "dataset_id": st_session_state.get("dataset_id"),
        "source_mode": st_session_state.get("source_mode", "both"),
    }
    # Include dataset rows if present (but not huge)
    dataset = st_session_state.get("dataset")
    if dataset and len(dataset) <= 500:
        payload["dataset"] = dataset

    try:
        with open(APP_STATE_FILE, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except Exception:
        pass


def load_app_state(st_session_state) -> None:
    if not os.path.exists(APP_STATE_FILE):
        return
    try:
        with open(APP_STATE_FILE, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        st_session_state.papers = _deserialize_papers(
            payload.get("papers", {}))
        st_session_state.active_paper_id = payload.get("active_paper_id")
        if st_session_state.active_paper_id not in st_session_state.papers:
            st_session_state.active_paper_id = next(
                iter(st_session_state.papers), None)
        # Restore dataset state
        st_session_state.dataset = payload.get("dataset")
        st_session_state.dataset_filename = payload.get("dataset_filename")
        st_session_state.dataset_id = payload.get("dataset_id")
        st_session_state.source_mode = payload.get("source_mode", "both")
    except Exception:
        pass

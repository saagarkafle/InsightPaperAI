from __future__ import annotations

import streamlit as st

from src.mvc.model import AppModel
from src.mvc.view import AppView


class AppController:
    def __init__(self, model: AppModel, view: AppView) -> None:
        self.model = model
        self.view = view

    def run(self) -> None:
        self.model.initialize()
        self.view.render_shell()

        if not self.model.has_any_source():
            result = self.view.render_landing_screen()
            uploaded_pdf = result.get("uploaded_pdf")
            uploaded_dataset = result.get("uploaded_dataset")
            process_requested = result.get("process_requested", False)

            if process_requested and (uploaded_pdf or uploaded_dataset):
                self._handle_processing(uploaded_pdf, uploaded_dataset)
        else:
            self.model.ensure_clients()
            tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate, reset_requested = (
                self.view.render_dashboard_screen()
            )
            self.view.render_tabs(
                tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate
            )
            if reset_requested:
                self.model.reset_current_session()
                st.rerun()

        self.view.render_footer()

    def _handle_processing(self, uploaded_pdf, uploaded_dataset) -> None:
        try:
            st.session_state.processing = True

            # ── Progress bar setup ──────────────────────────────────────────
            # Steps: [init clients, parse PDF, chunk+embed+upsert, summarise]
            # for PDF; dataset has slightly fewer steps.
            pdf_steps  = ["🔌 Connecting to services...",
                          "📄 Extracting text & figures from PDF...",
                          "🔢 Generating embeddings & indexing...",
                          "🧠 Generating paper summary..."]
            ds_steps   = ["🔌 Connecting to services...",
                          "📊 Reading & validating dataset...",
                          "🔢 Indexing dataset chunks..."]

            steps = pdf_steps if uploaded_pdf else ds_steps
            if uploaded_pdf and uploaded_dataset:
                steps = pdf_steps + ["📊 Indexing dataset..."]

            total_steps = len(steps)
            step_index  = [0]   # mutable for closure

            progress_bar  = st.progress(0, text=steps[0])
            status_text   = st.empty()

            def advance(msg: str = "") -> None:
                step_index[0] += 1
                pct = min(int(step_index[0] / total_steps * 100), 99)
                label = steps[min(step_index[0], total_steps - 1)]
                progress_bar.progress(pct, text=label)
                if msg:
                    status_text.caption(f"↳ {msg}")

            # ── Process uploads ─────────────────────────────────────────────
            if uploaded_pdf:
                self.model.process_uploaded_paper(
                    uploaded_pdf, progress=advance)

            if uploaded_dataset:
                success, error_msg = self.model.process_uploaded_dataset(
                    uploaded_dataset, progress=advance)
                if not success:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"Dataset error: {error_msg}")
                    st.session_state.processing = False
                    return

            # ── Done ────────────────────────────────────────────────────────
            progress_bar.progress(100, text="✅ Done!")
            status_text.empty()
            st.rerun()

        except Exception as error:
            st.error(f"Error: {error}")
        finally:
            st.session_state.processing = False


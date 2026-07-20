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
            with st.status("Processing uploads...", expanded=True) as status:
                # Process PDF if provided
                if uploaded_pdf:
                    self.model.process_uploaded_paper(
                        uploaded_pdf, progress=st.write)

                # Process dataset if provided
                if uploaded_dataset:
                    success, error_msg = self.model.process_uploaded_dataset(
                        uploaded_dataset, progress=st.write)
                    if not success:
                        st.error(f"Dataset error: {error_msg}")
                        st.session_state.processing = False
                        return

                # Build completion label
                parts = []
                if uploaded_pdf:
                    fig_count = len(
                        st.session_state.papers.get(
                            st.session_state.active_paper_id, {}
                        ).get("figures", [])
                    )
                    parts.append(f"Paper indexed, {fig_count} figures extracted")
                if uploaded_dataset:
                    row_count = len(st.session_state.get("dataset") or [])
                    parts.append(f"Dataset indexed ({row_count} rows)")

                status.update(
                    label=" · ".join(parts) + ".",
                    state="complete",
                )
            st.rerun()
        except Exception as error:
            st.error(f"Error: {error}")
        finally:
            st.session_state.processing = False

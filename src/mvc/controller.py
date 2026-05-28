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

        if not self.model.has_papers():
            uploaded_file, process_requested = self.view.render_landing_screen()
            if uploaded_file and process_requested:
                self._handle_paper_processing(uploaded_file)
        else:
            self.model.ensure_clients()
            tab_chat, tab_figures, tab_search, tab_stats, reset_requested = self.view.render_dashboard_screen()
            self.view.render_tabs(tab_chat, tab_figures, tab_search, tab_stats)
            if reset_requested:
                self.model.reset_current_session()
                st.rerun()

        self.view.render_footer()

    def _handle_paper_processing(self, uploaded_file) -> None:
        try:
            st.session_state.processing = True
            with st.status("Processing paper...", expanded=True) as status:
                self.model.process_uploaded_paper(
                    uploaded_file, progress=st.write)
                fig_count = len(
                    st.session_state.papers[st.session_state.active_paper_id].get("figures", []))
                status.update(
                    label=f"Paper indexed. {fig_count} figures extracted.",
                    state="complete",
                )
            st.rerun()
        except Exception as error:
            st.error(f"Error: {error}")
        finally:
            st.session_state.processing = False

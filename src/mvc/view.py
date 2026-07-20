from __future__ import annotations

from src.ui import (populate_tabs, render_css, render_dashboard, render_footer,
                    render_landing, render_navbar)


class AppView:
    def render_shell(self) -> None:
        render_css()
        render_navbar()

    def render_landing_screen(self):
        return render_landing()

    def render_dashboard_screen(self):
        return render_dashboard()

    def render_tabs(self, tab_chat, tab_figures, tab_search,
                    tab_stats, tab_evaluate) -> None:
        populate_tabs(tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate)

    def render_footer(self) -> None:
        render_footer()

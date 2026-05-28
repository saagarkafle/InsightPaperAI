import streamlit as st


def render_dashboard():
    reset_requested = False
    active_id = st.session_state.active_paper_id
    active_paper = st.session_state.papers.get(active_id, {})
    summary = active_paper.get("summary", {})
    paper_figures = active_paper.get("figures", [])

    dashboard_main, dashboard_right = st.columns([2.8, 0.72], gap="large")

    with dashboard_main:
        fig_count = len(paper_figures)
        st.markdown(f"""
        <div class="hero-card" style="margin-bottom:18px;">
            <div class="panel-kicker">Now reading</div>
            <div style="font-size:26px; font-weight:800; color:var(--text); margin-top:8px; line-height:1.2; letter-spacing:-0.9px;">{active_paper.get('title', 'Research Paper')[:90]}</div>
            <div class="hero-copy" style="margin-top:12px; max-width:none;">{active_paper.get('filename', '')} · {active_paper.get('word_count', 0):,} words · {active_paper.get('chunk_count', 0)} chunks · {active_paper.get('vectors_upserted', 0)} vectors · {fig_count} figures extracted</div>
        </div>
        """, unsafe_allow_html=True)

        # summary UI (kept concise)
        if summary:
            one_liner = summary.get("one_liner", "")
            problem = summary.get("problem", "")
            approach = summary.get("approach", "")
            diff = summary.get("difficulty", "Intermediate")
            field = summary.get("field", "")
            diff_class = f"diff-{diff.lower()}"

            findings = summary.get("key_findings", [])
            keywords = summary.get("keywords", [])

            findings_html = "".join(
                f"<div class='finding-item'>• {f}</div>" for f in findings[:3]) if findings else ""
            keywords_html = "".join(
                f"<span class='kw-tag'>{k}</span>" for k in keywords) if keywords else ""

            st.markdown(f"""
            <div class="overview-grid">
                <div class="card-glow" style="padding:22px;">
                    <div class="panel-title">Paper overview</div>
                    <div class="overview-copy" style="margin-bottom:14px;">{one_liner}</div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;"><span class="{diff_class}">{diff}</span><span class="pill-tag">{field}</span></div>
                    {"<div class='panel-copy' style='margin-bottom:8px;'><strong style='color:#f5f5f5;'>Problem:</strong> " + problem + "</div>" if problem else ""}
                    {"<div class='panel-copy'><strong style='color:#f5f5f5;'>Approach:</strong> " + approach + "</div>" if approach else ""}
                </div>
                <div class="panel"><div class="panel-title">Key findings</div><div class="findings-stack">{findings_html}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if keywords_html:
                st.markdown("<div style='height:12px'></div>",
                            unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="panel"><div class="panel-title">Topics</div><div>{keywords_html}</div></div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        tab_chat, tab_figures, tab_search, tab_stats = st.tabs(
            ["Ask Questions", f"Figures ({len(paper_figures)})", "Search", "Stats"])

    with dashboard_right:
        st.markdown(f"""
            <div class="panel compact"><div class="panel-title">Your library</div><div class="panel-copy" style="margin-bottom:12px;">Loaded paper</div>
        """, unsafe_allow_html=True)
        for paper_id, paper in st.session_state.papers.items():
            active_class = " active" if paper_id == active_id else ""
            st.markdown(f"""
                <div class="library-item{active_class}"><div class="library-title">{paper.get('title', 'Research Paper')[:72]}</div><div class="library-meta">{paper.get('chunk_count', 0)} chunks · {len(paper.get('figures', []))} figures</div></div>
            """, unsafe_allow_html=True)
        reset_requested = st.button(
            "Research new paper", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="panel compact"><div class="panel-title">Session stats</div>
                <div class="stat-card"><div class="stat-value">{len(st.session_state.messages)}</div><div class="stat-label">Messages</div></div>
                <div style="height:10px"></div>
                <div class="stat-card"><div class="stat-value">{len(paper_figures)}</div><div class="stat-label">Figures</div></div>
                <div style="height:10px"></div>
                <div class="stat-card"><div class="stat-value">{active_paper.get('chunk_count', 0)}</div><div class="stat-label">Chunks</div></div>
                <div class="stat-note">Use the center tabs to chat, inspect figures, and search semantically across the paper.</div>
            </div>
        """, unsafe_allow_html=True)

    # Return tabs so caller can populate chat/search/figures as needed
    return tab_chat, tab_figures, tab_search, tab_stats, reset_requested

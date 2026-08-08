import html as html_mod

import streamlit as st


@st.dialog("📄 Detailed Research Paper Summary", width="large")
def render_elaborated_summary_modal(active_paper):
    title = active_paper.get("title", "Research Paper")
    paper_text = active_paper.get("raw_text", "")
    summary_dict = active_paper.get("summary", {})

    st.markdown(f"### {html_mod.escape(title)}")
    st.caption("AI-generated 300 to 500 word comprehensive executive breakdown")
    st.markdown("---")

    elaborated = summary_dict.get("elaborated_summary")
    if not elaborated and paper_text:
        with st.spinner("Generating 300–500 word detailed executive summary..."):
            try:
                from src.llm_qa import generate_elaborated_summary, get_groq_client, resolve_model_id
                client = get_groq_client()
                model_id = resolve_model_id(st.session_state.get("selected_model"))
                elaborated = generate_elaborated_summary(paper_text, client, model_id)
                summary_dict["elaborated_summary"] = elaborated
                active_paper["summary"] = summary_dict
            except Exception as e:
                elaborated = f"Error generating summary: {e}"

    if elaborated:
        st.markdown(f"""
        <div style="
            background: #181818;
            border: 1px solid #282828;
            border-radius: 12px;
            padding: 22px;
            color: #FFFFFF;
            line-height: 1.7;
            font-size: 14px;
            max-height: 60vh;
            overflow-y: auto;
        ">
            {elaborated}
        </div>
        """, unsafe_allow_html=True)
        word_count = len(elaborated.split())
        st.markdown(f"<div style='margin-top:12px; font-size:12px; color:#A7A7A7;'>📊 Summary length: <strong>~{word_count} words</strong></div>", unsafe_allow_html=True)
    else:
        st.info("Full paper text is needed to generate the elaborated summary.")


def render_dashboard():
    """
    Render the dashboard screen with a two-column layout:
    - Narrow left sidebar: controls, stats, source toggle
    - Wide right main area: paper overview, tab content
    """
    reset_requested = False
    active_id = st.session_state.active_paper_id
    active_paper = st.session_state.papers.get(active_id, {})
    summary = active_paper.get("summary", {})
    paper_figures = active_paper.get("figures", [])
    has_dataset = bool(st.session_state.get("dataset"))
    dataset_filename = st.session_state.get("dataset_filename", "")

    dashboard_main, dashboard_right = st.columns([2.8, 0.8], gap="large")

    with dashboard_main:
        # ─── Paper Header Card ───
        if active_paper:
            fig_count = len(paper_figures)
            paper_title = html_mod.escape(
                active_paper.get("title", "Research Paper")[:90])
            paper_filename = html_mod.escape(
                active_paper.get("filename", ""))
            word_count = active_paper.get("word_count", 0)
            chunk_count = active_paper.get("chunk_count", 0)
            vectors = active_paper.get("vectors_upserted", 0)

            st.markdown(f"""
            <div class="hero-card">
                <div class="panel-kicker">Now reading</div>
                <div style="font-size:24px; font-weight:800; color:var(--text); margin-top:8px; line-height:1.2; letter-spacing:-0.6px;">{paper_title}</div>
            </div>
            """, unsafe_allow_html=True)
        elif has_dataset:
            safe_ds_name = html_mod.escape(dataset_filename)
            ds_rows = len(st.session_state.get("dataset") or [])
            st.markdown(f"""
            <div class="hero-card">
                <div class="panel-kicker">Dataset loaded</div>
                <div style="font-size:24px; font-weight:800; color:var(--text); margin-top:8px; line-height:1.2; letter-spacing:-0.6px;">📊 {safe_ds_name}</div>
            </div>
            """, unsafe_allow_html=True)

        # ─── Summary Section ───
        if summary:
            one_liner = html_mod.escape(summary.get("one_liner", ""))
            problem = html_mod.escape(summary.get("problem", ""))
            approach = html_mod.escape(summary.get("approach", ""))
            diff = summary.get("difficulty", "Intermediate")
            field = html_mod.escape(summary.get("field", ""))
            diff_class = f"diff-{diff.lower()}"

            findings = summary.get("key_findings", [])
            keywords = summary.get("keywords", [])

            findings_html = "".join(
                f"<div class='finding-item'>• {html_mod.escape(f)}</div>"
                for f in findings[:3]
            ) if findings else ""
            keywords_html = "".join(
                f"<span class='kw-tag'>{html_mod.escape(k)}</span>"
                for k in keywords
            ) if keywords else ""

            st.markdown(f"""
            <div class="overview-grid">
                <div class="card" style="border-left: 3px solid var(--accent);">
                    <div class="panel-title">Paper overview</div>
                    <div class="overview-copy" style="margin-bottom:14px;">{one_liner}</div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;"><span class="{diff_class}">{html_mod.escape(diff)}</span><span class="pill-tag">{field}</span></div>
                    {"<div style='color:var(--text-secondary); font-size:14px; margin-bottom:8px;'><strong>Problem:</strong> " + problem + "</div>" if problem else ""}
                    {"<div style='color:var(--text-secondary); font-size:14px;'><strong>Approach:</strong> " + approach + "</div>" if approach else ""}
                </div>
                <div class="card"><div class="panel-title">Key findings</div><div class="findings-stack">{findings_html}</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Button to open 300-500 word elaborated summary modal
            if st.button("📖 Read Elaborated Summary (300–500 words)", key="btn_elaborated_modal", use_container_width=True):
                render_elaborated_summary_modal(active_paper)

            if keywords_html:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="card"><div class="panel-title">Topics</div><div>{keywords_html}</div></div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ─── Vertical Tab Navigation + Content ───
        nav_col, content_col = st.columns([0.85, 2.6], gap="large")

        if 'selected_tab' not in st.session_state:
            st.session_state['selected_tab'] = 'Ask Questions'

        options = [
            'Ask Questions',
            f'Figures ({len(paper_figures)})',
            'Search',
            'Stats',
        ]
        if has_dataset:
            options.append('Evaluate')

        with nav_col:
            st.markdown("<div class='vertical-tabbar'>", unsafe_allow_html=True)
            try:
                idx = options.index(st.session_state.get('selected_tab', options[0]))
            except ValueError:
                idx = 0
            selected = st.radio("", options=options, index=idx, key="vertical_nav")
            st.session_state['selected_tab'] = selected
            st.markdown("</div>", unsafe_allow_html=True)

        with content_col:
            tab_chat = st.container()
            tab_figures = st.container()
            tab_search = st.container()
            tab_stats = st.container()
            tab_evaluate = st.container()

    # ─── Right Sidebar ───
    with dashboard_right:
        # ─── Model Selector (Concise Dashboard Labels) ───
        dashboard_model_names = ["Qwen (Deep Analysis)", "LLaMA (Fast Inference)"]
        current_model = st.session_state.get("selected_model", "")
        if "llama" in str(current_model).lower():
            model_idx = 1
        else:
            model_idx = 0

        selected_model = st.selectbox(
            "LLM Model",
            options=dashboard_model_names,
            index=model_idx,
            key="dashboard_model_select",
        )
        st.session_state.selected_model = selected_model
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # ─── Source Mode Toggle ───
        has_pdf = bool(st.session_state.papers)
        if has_pdf and has_dataset:
            current_mode = st.session_state.get("source_mode", "both")
            mode_options = ["Both", "PDF only", "Dataset only"]
            mode_map = {"both": "Both", "pdf": "PDF only", "dataset": "Dataset only"}
            reverse_map = {"Both": "both", "PDF only": "pdf", "Dataset only": "dataset"}
            current_label = mode_map.get(current_mode, "Both")

            source_mode = st.radio(
                "Source Mode",
                options=mode_options,
                index=mode_options.index(current_label),
                key="dashboard_source_mode",
            )
            st.session_state.source_mode = reverse_map.get(source_mode, "both")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        reset_requested = st.button(
            "Start new session", use_container_width=True)

    return tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate, reset_requested

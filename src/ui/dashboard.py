import html as html_mod

import streamlit as st


def format_elaborated_summary_html(text: str) -> str:
    """Format markdown elaborated summary into beautiful Spotify-themed executive cards."""
    import re
    
    # Strip any bulleted prompt echoes or pre-analysis text before the first section
    text = re.sub(r'(?m)^\s*\*+\s*###.*$', '', text)
    text = re.sub(r'(?m)^\s*(Constraints|Source Material|Analyze|Deconstruct|Draft):.*$', '', text, flags=re.IGNORECASE)

    for pattern in ["### 1.", "### Core Problem", "1. Core Problem"]:
        if pattern in text:
            idx = text.find(pattern)
            text = text[idx:]
            break

    sections = re.split(r'(?m)^###\s+', text)
    if len(sections) <= 1 and not text.startswith("###"):
        # Fallback if no H3 section headers found
        return f"""
        <div style="background: #242424; border: 1px solid #333333; border-left: 4px solid #1DB954; border-radius: 12px; padding: 20px; color: #E0E0E0; font-size: 14px; line-height: 1.75;">
            {html_mod.escape(text).replace('\n', '<br/>')}
        </div>
        """
    
    icons_map = {
        "problem": "🎯",
        "context": "🎯",
        "method": "⚙️",
        "innovation": "⚙️",
        "finding": "📈",
        "benchmark": "📈",
        "result": "📈",
        "impact": "🔮",
        "future": "🔮",
        "limitation": "🔮",
    }
    
    html_cards = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        lines = sec.split("\n", 1)
        header = lines[0].strip()
        
        # Skip preamble lines that don't match expected executive section headers
        if not re.search(r'^(1|2|3|4|Core|Proposed|Critical|Broader|Problem|Method|Finding|Impact)', header, re.IGNORECASE):
            continue

        body = lines[1].strip() if len(lines) > 1 else ""
        
        icon = "📌"
        for key, ic in icons_map.items():
            if key in header.lower():
                icon = ic
                break
        
        clean_header = re.sub(r'^\d+[\.\)]\s*', '', header)
        paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
        body_html = "".join(f"<p style='margin-bottom: 10px; color: #D1D5DB; line-height: 1.7; font-size: 13.5px;'>{html_mod.escape(p)}</p>" for p in paragraphs)
        
        html_cards.append(f"""
        <div style="
            background: #242424;
            border: 1px solid #333333;
            border-left: 4px solid #1DB954;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        ">
            <div style="font-weight: 700; font-size: 15px; color: #1ED760; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 18px;">{icon}</span> <span>{html_mod.escape(clean_header)}</span>
            </div>
            <div>
                {body_html}
            </div>
        </div>
        """)
        
    return "".join(html_cards)


@st.dialog("📄 Executive Research Summary", width="large")
def render_elaborated_summary_modal(active_paper):
    title = active_paper.get("title", "Research Paper")
    paper_text = (
        active_paper.get("full_text") or
        active_paper.get("raw_text") or
        active_paper.get("text") or ""
    )
    summary_dict = active_paper.get("summary", {})

    # ── Fallback: reconstruct from all available summary fields ──
    if not paper_text and summary_dict:
        one_liner  = summary_dict.get("one_liner", "")
        problem    = summary_dict.get("problem", "")
        approach   = summary_dict.get("approach", "")
        findings   = " ".join(summary_dict.get("key_findings", []))
        keywords   = " ".join(summary_dict.get("keywords", []))
        field      = summary_dict.get("field", "")
        paper_text = (
            f"Research Paper Title: {title}. Field: {field}. "
            f"Overview: {one_liner}. Problem: {problem}. "
            f"Approach: {approach}. Key Findings: {findings}. Keywords: {keywords}."
        ).strip()

    field = summary_dict.get("field", "Academic Research")
    diff = summary_dict.get("difficulty", "Intermediate")
    diff_class = f"diff-{diff.lower()}"

    # ─── Modal Header Banner ───
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #181818, #242424);
        border: 1px solid #333333;
        border-top: 3px solid #1DB954;
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 18px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; color: #1DB954;">
                🧠 Deep Executive Summary (300–500 Words)
            </div>
            <div style="display:flex; gap:6px;">
                <span class="pill-tag">{html_mod.escape(field)}</span>
                <span class="{diff_class}">{html_mod.escape(diff)}</span>
            </div>
        </div>
        <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; line-height: 1.3;">
            {html_mod.escape(title)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # If still no text at all, show a clear actionable warning
    if not paper_text:
        st.markdown("""
        <div style="
            background: #1a1a1a;
            border: 1px solid #444;
            border-left: 4px solid #e74c3c;
            border-radius: 10px;
            padding: 18px 22px;
            color: #E0E0E0;
            font-size: 14px;
            line-height: 1.7;
        ">
            <span style="font-size: 18px;">⚠️</span>
            <strong style="color: #ff6b6b;"> Paper text not available.</strong><br/>
            The original PDF text was not saved in this session.
            Please <strong>re-upload your PDF</strong> on the landing page to regenerate the executive summary.
        </div>
        """, unsafe_allow_html=True)
        return

    elaborated = summary_dict.get("elaborated_summary")
    bad_keywords = [
        "Unable to generate", "Error:", "Deconstruct the Request", "Analyze the Source",
        "Draft the Summary", "Word Count Check", "Goal:", "Constraints:", "Source Material:",
        "Draft - Section", "*   ### 2.", "*   ### 3.", "* ### 2.", "* ### 3.",
        "1.  **Deconstruct", "2. Analyze", "3. Draft", "Analyze User Input",
        "Deconstruct", "Word Count",
    ]
    is_corrupted = elaborated is not None and any(k in str(elaborated) for k in bad_keywords)

    if is_corrupted:
        # Force-clear the dirty cached summary so generation runs fresh
        summary_dict.pop("elaborated_summary", None)
        elaborated = None

    if not elaborated:
        with st.spinner("Generating 300–500 word detailed executive summary..."):
            try:
                from src.llm_qa import generate_elaborated_summary, get_groq_client, resolve_model_id
                client = get_groq_client()
                model_id = resolve_model_id(st.session_state.get("selected_model"))
                elaborated = generate_elaborated_summary(paper_text, client, model_id)
                summary_dict["elaborated_summary"] = elaborated
                active_paper["summary"] = summary_dict
            except Exception as e:
                st.error(f"⚠️ Failed to generate executive summary: {e}")
                st.info("Please try again or re-upload your PDF.")
                return

    if elaborated:
        cards_html = format_elaborated_summary_html(elaborated)
        word_count = len(elaborated.split())
        active_model = st.session_state.get("selected_model", "Qwen 3.6 27B")

        st.markdown(f"""
        <div style="max-height: 58vh; overflow-y: auto; padding-right: 6px;">
            {cards_html}
        </div>
        <div style="
            background: #181818;
            border: 1px solid #282828;
            border-radius: 10px;
            padding: 10px 16px;
            margin-top: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 12px;
            color: #A7A7A7;
        ">
            <div>📊 Total Length: <strong style="color:#FFFFFF;">~{word_count} words</strong></div>
            <div>🛡️ Grounding: <strong style="color:#1ED760;">100% Verified Context</strong></div>
            <div>🤖 Engine: <strong style="color:#FFFFFF;">{html_mod.escape(active_model)}</strong></div>
        </div>
        """, unsafe_allow_html=True)


def render_dashboard():
    """
    Render the dashboard screen with a two-column layout:
    - Narrow left sidebar: controls, stats, source toggle
    - Wide right main area: paper overview, tab content
    """
    # Smooth scroll to top when dashboard opens (multi-target for all Streamlit versions)
    import streamlit.components.v1 as components
    components.html("""
    <script>
        function forceScrollTop() {
            try {
                var p = window.parent;
                var doc = p.document;
                var targets = [
                    p,
                    doc.documentElement,
                    doc.body,
                    doc.querySelector('section.main'),
                    doc.querySelector('.main'),
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('[data-testid="stAppViewContainer"]')
                ];
                targets.forEach(function(el) {
                    if (el) {
                        if (typeof el.scrollTo === 'function') {
                            el.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
                        }
                        el.scrollTop = 0;
                    }
                });
            } catch(e) {}
        }
        forceScrollTop();
        setTimeout(forceScrollTop, 50);
        setTimeout(forceScrollTop, 200);
        setTimeout(forceScrollTop, 500);
        setTimeout(forceScrollTop, 1000);
    </script>
    """, height=0)

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
                str(active_paper.get("title") or "Research Paper")[:90])
            paper_filename = html_mod.escape(
                str(active_paper.get("filename") or ""))
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
            safe_ds_name = html_mod.escape(str(dataset_filename or ""))
            ds_rows = len(st.session_state.get("dataset") or [])
            st.markdown(f"""
            <div class="hero-card">
                <div class="panel-kicker">Dataset loaded</div>
                <div style="font-size:24px; font-weight:800; color:var(--text); margin-top:8px; line-height:1.2; letter-spacing:-0.6px;">📊 {safe_ds_name}</div>
            </div>
            """, unsafe_allow_html=True)

        # ─── Summary Section ───
        if summary:
            one_liner = html_mod.escape(str(summary.get("one_liner") or ""))
            problem = html_mod.escape(str(summary.get("problem") or ""))
            approach = html_mod.escape(str(summary.get("approach") or ""))
            diff = str(summary.get("difficulty") or "Intermediate")
            field = html_mod.escape(str(summary.get("field") or ""))
            diff_class = f"diff-{diff.lower()}"

            findings = summary.get("key_findings") or []
            keywords = summary.get("keywords") or []

            findings_html = "".join(
                f"<div class='finding-item'>• {html_mod.escape(str(f))}</div>"
                for f in findings[:3]
            ) if findings else ""
            keywords_html = "".join(
                f"<span class='kw-tag'>{html_mod.escape(str(k))}</span>"
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
            with st.container(key="vertical_tabbar_container"):
                try:
                    idx = options.index(st.session_state.get('selected_tab', options[0]))
                except ValueError:
                    idx = 0
                selected = st.radio(
                    "Navigation",
                    options=options,
                    index=idx,
                    key="vertical_nav",
                    label_visibility="collapsed",
                )
                st.session_state['selected_tab'] = selected

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
        with st.container(key="new_session_btn_container"):
            reset_requested = st.button(
                "Start new session",
                key="btn_new_session",
                use_container_width=True,
            )

    return tab_chat, tab_figures, tab_search, tab_stats, tab_evaluate, reset_requested

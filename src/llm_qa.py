# src/llm_qa.py — LLM Question Answering with RAG Context
import os
import re
import time
from dataclasses import dataclass

import openai

from src.llm_utils import parse_json_response, strip_think_tags


# ─────────────────────────────────────────────
# AVAILABLE MODELS (served via Groq)
# ─────────────────────────────────────────────
AVAILABLE_MODELS = {
    "Qwen 3.6 27B (Deep Analysis)": "qwen/qwen3.6-27b",
    "LLaMA 3.1 8B (Fast Inference)": "llama-3.1-8b-instant",
}

DEFAULT_MODEL = "Qwen 3.6 27B (Deep Analysis)"


def resolve_model_id(display_name: str | None = None) -> str:
    """Resolve a human-readable model display name to its Groq model ID."""
    name = display_name or DEFAULT_MODEL
    if "llama" in name.lower():
        return "llama-3.1-8b-instant"
    return "qwen/qwen3.6-27b"


@dataclass
class QAResponse:
    answer: str
    sources: list[dict]
    tokens_in: int
    tokens_out: int
    latency_ms: float
    model: str


# ─────────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────────
def get_groq_client() -> openai.OpenAI:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("groq_api_key")
            if api_key:
                os.environ["GROQ_API_KEY"] = api_key
        except Exception:
            pass

    if not api_key:
        raise ValueError("GROQ_API_KEY not set in environment or Streamlit secrets. Please add it to your .env file or Streamlit Cloud Secrets.")

    return openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )


# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AI research assistant specializing in analyzing academic papers.

You answer questions based STRICTLY on the provided context from the research paper(s) and/or datasets.

RULES:
1. Only use information from the provided context — never fabricate or assume facts.
2. If the answer is not in the context, say: "This information is not covered in the provided paper sections."
3. Always be specific — cite actual details, numbers, and findings from the paper.
4. Structure your answers clearly:
   - Start with a direct answer
   - Follow with supporting evidence from the paper
   - End with your analytical insight if relevant
5. For technical questions, explain concepts clearly without oversimplifying.
6. If asked to compare or summarize, be comprehensive but concise.
7. When context comes from multiple source types (PDF and Dataset), clearly indicate
   which source type each piece of information came from using labels like
   "According to the PDF..." or "From the dataset...".
8. NEVER include your inner thinking process, reasoning steps, or <think> tags. Output ONLY your final grounded answer directly to the user.

You are talking to a researcher who wants deep, accurate insights — not surface-level summaries.
"""


# ─────────────────────────────────────────────
# BUILD CONTEXT FROM RETRIEVED CHUNKS
# ─────────────────────────────────────────────
def build_context(retrieved_chunks: list[dict], max_tokens: int = 3000) -> str:
    """
    Build a clean context string from retrieved chunks.
    Deduplicates and orders by relevance score.
    Labels each source with its source_type (PDF or Dataset).
    """
    # Sort by score descending
    sorted_chunks = sorted(
        retrieved_chunks, key=lambda x: x["score"], reverse=True)

    context_parts = []
    total_words = 0

    for i, chunk in enumerate(sorted_chunks):
        text = chunk["text"].strip()
        words = len(text.split())

        if total_words + words > max_tokens:
            break

        # Determine source label
        source_type = chunk.get("source_type", "pdf")
        if source_type == "dataset":
            type_label = "📊 Dataset"
        else:
            type_label = "📄 PDF"

        context_parts.append(
            f"[Source {i+1} | {type_label} | Paper: {chunk['paper_title']} | Relevance: {chunk['score']}]\n{text}"
        )
        total_words += words

    return "\n\n---\n\n".join(context_parts)


# ─────────────────────────────────────────────
# MAIN QA FUNCTION
# ─────────────────────────────────────────────
def answer_question(
    question: str,
    retrieved_chunks: list[dict],
    client: openai.OpenAI,
    model: str = "qwen/qwen3.6-27b",
    max_tokens: int = 2048,
) -> QAResponse:
    """
    Generate an answer using RAG context + LLM.
    """
    context = build_context(retrieved_chunks)

    user_message = f"""Based on the following context from the research paper(s), answer this question:

QUESTION: {question}

CONTEXT:
{context}

Provide a detailed, accurate answer based strictly on the context above."""

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
        max_tokens=max_tokens,
    )
    latency_ms = (time.time() - start) * 1000

    answer = strip_think_tags(response.choices[0].message.content)
    usage = response.usage

    return QAResponse(
        answer=answer,
        sources=retrieved_chunks,
        tokens_in=usage.prompt_tokens,
        tokens_out=usage.completion_tokens,
        latency_ms=latency_ms,
        model=model
    )


# ─────────────────────────────────────────────
# PAPER SUMMARY GENERATOR
# ─────────────────────────────────────────────
def generate_paper_summary(paper_text: str, client: openai.OpenAI,
                           model: str = "qwen/qwen3.6-27b") -> dict:
    """Generate structured summary of a research paper."""
    prompt = f"""Analyze this research paper and return a JSON object with these exact keys:
{{
  "title_detected": "paper title if you can detect it",
  "one_liner": "one sentence describing what this paper does",
  "problem": "what problem does this paper solve",
  "approach": "what method/approach do they use",
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "limitations": ["limitation 1", "limitation 2"],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "difficulty": "Beginner / Intermediate / Advanced",
  "field": "e.g. NLP, Computer Vision, Reinforcement Learning, etc."
}}

Return ONLY valid JSON. No markdown, no explanation.

Paper text (first 3000 words):
{" ".join(paper_text.split()[:3000])}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at analyzing research papers. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4096,
        )
        return parse_json_response(response.choices[0].message.content)
    except Exception as primary_error:
        # Fallback to llama-3.1-8b-instant if primary model summary generation failed
        try:
            fallback_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing research papers. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000,
            )
            return parse_json_response(fallback_response.choices[0].message.content)
        except Exception:
            return {
                "title_detected": "Unknown",
                "one_liner": "Summary unavailable",
                "problem": "",
                "approach": "",
                "key_findings": [],
                "limitations": [],
                "keywords": [],
                "difficulty": "Unknown",
                "field": "Unknown"
            }


# ─────────────────────────────────────────────
# ELABORATED SUMMARY GENERATOR (300-500 WORDS)
# ─────────────────────────────────────────────
def _clean_summary_output(raw_text: str) -> str:
    """Aggressively clean LLM output to start ONLY at '### 1. Core Problem'."""
    text = strip_think_tags(raw_text)

    # Find the FIRST occurrence of the actual section 1 header (with ### prefix)
    # This is the definitive start of the real summary content.
    h3_match = re.search(r"(?m)^###\s+1[\.\)]?\s+Core Problem", text)
    if h3_match:
        text = text[h3_match.start():]
        return text.strip()

    # Fallback: find "### 1." in any form
    h3_fallback = re.search(r"(?m)^###\s+1[\.\)]?", text)
    if h3_fallback:
        text = text[h3_fallback.start():]
        return text.strip()

    # Last resort: strip all numbered-list preamble lines (e.g. "1. **Deconstruct...", "2. Analyze...")
    # Remove lines beginning with number+dot or number+asterisk patterns until we hit real content
    text = re.sub(r"(?ms)^(\d+[\.\)]\s+.*?)((?=^###)|\Z)", "", text)
    text = re.sub(r"(?m)^\s*\*+\s*###.*$", "", text)
    text = re.sub(r"(?m)^\s*(Constraints|Source Material|Analyze|Deconstruct|Draft|Goal):.*$", "", text, flags=re.IGNORECASE)

    return text.strip()


def generate_elaborated_summary(paper_text: str, client: openai.OpenAI,
                                 model: str = "qwen/qwen3.6-27b") -> str:
    """Generate a 300-500 word comprehensive executive summary of a research paper."""
    words = paper_text.split()
    excerpt = " ".join(words[:1800]) if len(words) > 1800 else paper_text

    prompt = f"""Write a comprehensive, highly detailed 300 to 500 word executive summary of this research paper.

DO NOT output any prompt repetition, bulleted lists of headings, planning steps, deconstruction steps, or introductory text.
START IMMEDIATELY WITH:
### 1. Core Problem & Research Context

Write 4 markdown sections:
### 1. Core Problem & Research Context
Explain the primary problem, research gap, and motivation behind this work.

### 2. Proposed Methodology & Key Innovations
Detail the key technical approach, architecture, dataset, or mathematical framework introduced.

### 3. Critical Findings & Experimental Benchmarks
Summarize the quantitative findings, baseline comparisons, and main performance metrics achieved.

### 4. Broader Impact, Limitations & Future Work
Explain the practical significance of this paper, its limitations, and potential future research directions.

Target between 350 and 450 words total. Keep the summary thorough, academic, clear, and grounded exclusively in the paper content.

Paper text excerpt:
{excerpt}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a senior academic researcher. Write ONLY the 4 markdown summary sections. Start immediately with ### 1. Core Problem & Research Context. No thinking, no analysis steps, no reasoning, no planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            reasoning_effort="none",
        )
        return _clean_summary_output(response.choices[0].message.content)
    except Exception:
        try:
            fallback = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a senior academic researcher. Write ONLY the 4 markdown summary sections. Start immediately with ### 1. Core Problem & Research Context. No thinking, no analysis steps, no reasoning, no planning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=900,
                reasoning_effort="none",
            )
            return _clean_summary_output(fallback.choices[0].message.content)
        except Exception as e:
            return f"Unable to generate elaborated summary: {e}"


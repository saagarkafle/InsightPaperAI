# src/llm_utils.py — Shared LLM response cleaning utilities
import json
import re


def strip_think_tags(text: str) -> str:
    """Remove <think>…</think> blocks from LLM responses (e.g. Qwen reasoning)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def parse_json_response(raw: str) -> dict:
    """
    Clean an LLM response and extract a JSON object.

    Steps:
      1. Strip <think>…</think> reasoning blocks
      2. Remove Markdown JSON fences (```json … ```)
      3. Extract the first {…} object via regex
      4. Parse as JSON

    Raises ValueError if no valid JSON is found.
    """
    cleaned = strip_think_tags(raw)
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(0)

    return json.loads(cleaned)

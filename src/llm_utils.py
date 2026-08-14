# src/llm_utils.py — Shared LLM response cleaning utilities
import json
import re


def strip_think_tags(text: str) -> str:
    """Remove all forms of <think>…</think> and reasoning blocks from LLM responses."""
    if not text:
        return ""

    # 1. Remove closed XML/HTML style tags like <think>...</think>, <thought>...</thought>, etc.
    cleaned = re.sub(r"<(think|thought|reasoning|details)>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # 2. Remove unclosed opening tags at the start of text (e.g. <think> ...)
    cleaned = re.sub(r"^\s*<(think|thought|reasoning|details)>.*?(?=\n\n|\n#|\Z)", "", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # 3. Remove "Thinking Process:" or "Reasoning:" text prefixes
    cleaned = re.sub(r"^\s*(\*\*|\*)?(Thinking Process|Thought Process|Thinking|Reasoning):?(\*\*|\*)?.*?(?=\n\n|\n#|\Z)", "", cleaned, flags=re.DOTALL | re.IGNORECASE)

    # 4. Remove any stray trailing </think>, </thought>, etc.
    cleaned = re.sub(r"</(think|thought|reasoning|details)>", "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


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

# src/dataset_parser.py — CSV/JSON Dataset Parser & Validator
import csv
import hashlib
import io
import json
from typing import Optional


def normalize_row_schema(row: dict) -> dict:
    """
    Normalize row keys to lowercase and map Kaggle research paper dataset columns
    (Title, Abstract, AI-Generated Summary, Keywords, Field) to standard question, answer, context.
    """
    norm = {k.strip().lower(): str(v).strip() for k, v in row.items() if k}
    title = norm.get("title", "")
    abstract = norm.get("abstract", "")
    ai_summary = norm.get("ai-generated summary", "") or norm.get("ai_generated_summary", "") or norm.get("summary", "")
    keywords = norm.get("keywords", "")
    field = norm.get("field", "")

    if title or abstract or ai_summary:
        if "question" not in norm and title:
            q_str = f"Summarize the main contribution and key findings of the research paper titled '{title}'."
            if keywords:
                q_str += f" Keywords: {keywords}."
            norm["question"] = q_str
        if "answer" not in norm:
            norm["answer"] = ai_summary if ai_summary else abstract
        if "context" not in norm:
            ctx_parts = []
            if title:
                ctx_parts.append(f"Title: {title}")
            if field:
                ctx_parts.append(f"Field: {field}")
            if keywords:
                ctx_parts.append(f"Keywords: {keywords}")
            if abstract:
                ctx_parts.append(f"Abstract: {abstract}")
            norm["context"] = "\n".join(ctx_parts)
    return norm


def parse_csv(file_content: bytes) -> list[dict]:
    """Parse a CSV file with columns: question, answer, context (optional) or Kaggle research paper columns."""
    text = file_content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        rows.append(normalize_row_schema(row))
    return rows


def parse_json_dataset(file_content: bytes) -> list[dict]:
    """Parse a JSON file containing an array of objects."""
    text = file_content.decode("utf-8", errors="replace")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("JSON must be an array of objects.")
    rows = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the JSON array must be an object.")
        rows.append(normalize_row_schema(item))
    return rows


def validate_dataset(rows: list[dict]) -> tuple[bool, str]:
    """
    Validate that the dataset has the required columns.
    Returns (is_valid, error_message).
    """
    if not rows:
        return False, "Dataset is empty — no rows found."

    first_row = rows[0]
    if "question" not in first_row:
        return False, "Missing required column: 'question' or 'title'. Found columns: " + ", ".join(first_row.keys())
    if "answer" not in first_row:
        return False, "Missing required column: 'answer' or 'ai-generated summary'. Found columns: " + ", ".join(first_row.keys())

    # Check for non-empty values in at least one row
    has_content = False
    for row in rows:
        if row.get("question", "").strip() and row.get("answer", "").strip():
            has_content = True
            break

    if not has_content:
        return False, "All rows have empty question or answer fields."

    return True, ""


def dataset_to_chunks(rows: list[dict]) -> list[str]:
    """
    Extract indexable text chunks from dataset rows.
    Uses 'context' field if available, otherwise falls back to 'answer'.
    """
    chunks = []
    for row in rows:
        context = row.get("context", "").strip()
        if context:
            chunks.append(context)
        else:
            answer = row.get("answer", "").strip()
            if answer:
                chunks.append(answer)
    return chunks


def make_dataset_id(filename: str) -> str:
    """Generate a short unique ID for a dataset file."""
    return "ds_" + hashlib.md5(filename.encode()).hexdigest()[:12]


def get_preview_rows(rows: list[dict], n: int = 5) -> list[dict]:
    """Return the first n rows for preview display."""
    return rows[:n]

# src/dataset_parser.py — CSV/JSON Dataset Parser & Validator
import csv
import hashlib
import io
import json
from typing import Optional


def parse_csv(file_content: bytes) -> list[dict]:
    """Parse a CSV file with columns: question, answer, context (optional)."""
    text = file_content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        # Normalize column names to lowercase
        normalized = {k.strip().lower(): v.strip() for k, v in row.items() if k}
        rows.append(normalized)
    return rows


def parse_json_dataset(file_content: bytes) -> list[dict]:
    """Parse a JSON file containing an array of {question, answer, context} objects."""
    text = file_content.decode("utf-8", errors="replace")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("JSON must be an array of objects.")
    rows = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the JSON array must be an object.")
        normalized = {k.strip().lower(): str(v).strip() for k, v in item.items() if k}
        rows.append(normalized)
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
        return False, "Missing required column: 'question'. Found columns: " + ", ".join(first_row.keys())
    if "answer" not in first_row:
        return False, "Missing required column: 'answer'. Found columns: " + ", ".join(first_row.keys())

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

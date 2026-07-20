# src/ui/dataset_handler.py
import csv
import io
import json

from src.rag_pipeline import upsert_dataset


def parse_dataset(file_content: bytes, filename: str) -> list[dict]:
    """
    Parses a CSV or JSON file into a list of dictionaries.
    """
    rows = []
    try:
        content_str = file_content.decode("utf-8")
        if filename.lower().endswith(".csv"):
            reader = csv.DictReader(io.StringIO(content_str))
            for row in reader:
                # Strip keys and values
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k and v}
                rows.append(clean_row)
        elif filename.lower().endswith(".json"):
            data = json.loads(content_str)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        clean_item = {k.strip(): str(v).strip() for k, v in item.items() if k and v}
                        rows.append(clean_item)
            else:
                raise ValueError("JSON file must contain an array of objects.")
        else:
            raise ValueError("Unsupported file type. Must be .csv or .json.")
    except Exception as e:
        raise ValueError(f"Error parsing dataset: {e}")
    
    return rows


def validate_dataset(rows: list[dict]) -> tuple[bool, str]:
    """
    Validates that the dataset contains 'question' and 'answer' columns.
    """
    if not rows:
        return False, "Dataset is empty or could not be parsed."
    
    first_row = rows[0]
    required_cols = {"question", "answer"}
    
    # Convert keys to lowercase for case-insensitive check
    lower_keys = {k.lower() for k in first_row.keys()}
    
    missing = required_cols - lower_keys
    if missing:
        return False, f"Dataset is missing required columns: {', '.join(missing)}"
    
    return True, ""


def index_dataset(rows: list[dict], filename: str, embedder, index) -> int:
    """
    Extracts chunks from the dataset (preferring 'context', falling back to 'answer'),
    and indexes them into Pinecone. Returns the number of vectors indexed.
    """
    chunks = []
    for row in rows:
        # Standardize keys to lowercase
        lower_row = {k.lower(): v for k, v in row.items()}
        
        # Prefer context, fallback to answer
        chunk_text = lower_row.get("context", "")
        if not chunk_text.strip():
            chunk_text = lower_row.get("answer", "")
            
        if chunk_text.strip():
            chunks.append(chunk_text.strip())
            
    if not chunks:
        return 0

    # Using the existing upsert_dataset function from rag_pipeline which automatically
    # sets source_type="dataset".
    import hashlib
    dataset_id = hashlib.md5(filename.encode()).hexdigest()[:12]
    
    vector_count = upsert_dataset(
        dataset_id=dataset_id,
        dataset_name=filename,
        chunks=chunks,
        embedder=embedder,
        index=index
    )
    
    return vector_count

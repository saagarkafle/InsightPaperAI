# src/rag_pipeline.py — RAG Pipeline with sentence-transformers
import hashlib
import os
import time
from typing import Optional

from pinecone import Pinecone, ServerlessSpec

_model = None

# Path where the fine-tuned model is saved by scripts/finetune_embedder.py
_FINE_TUNED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "models", "fine_tuned_embedder"
)
_BASE_MODEL = "all-MiniLM-L6-v2"


def get_embedder(model_name_or_path: Optional[str] = None):
    global _model
    from sentence_transformers import SentenceTransformer
    if model_name_or_path is not None:
        print(f"[embedder] Loading specified model: {model_name_or_path}")
        return SentenceTransformer(model_name_or_path)

    if _model is None:
        if os.path.isdir(_FINE_TUNED_PATH):
            print(f"[embedder] Loading fine-tuned model from {_FINE_TUNED_PATH}")
            _model = SentenceTransformer(_FINE_TUNED_PATH)
        else:
            print(f"[embedder] Loading base model: {_BASE_MODEL}")
            _model = SentenceTransformer(_BASE_MODEL)
    return _model


def embed_texts(texts: list[str], embedder) -> list[list[float]]:
    """Encode a batch of text strings into embedding vectors."""
    vectors = embedder.encode(texts, show_progress_bar=False, batch_size=32)
    return vectors.tolist()


def embed_query(query: str, embedder) -> list[float]:
    """Encode a single query string into an embedding vector."""
    vector = embedder.encode([query], show_progress_bar=False)
    return vector[0].tolist()


def get_pinecone_index(index_name: str = "research-papers"):
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("PINECONE_API_KEY") or st.secrets.get("pinecone_api_key")
            if api_key:
                os.environ["PINECONE_API_KEY"] = api_key
        except Exception:
            pass

    if not api_key:
        raise ValueError("PINECONE_API_KEY not set in environment or Streamlit secrets. Please add it to your .env file or Streamlit Cloud Secrets.")

    pc = Pinecone(api_key=api_key)
    existing = [i.name for i in pc.list_indexes()]

    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    else:
        info = pc.describe_index(index_name)
        if info.dimension != 384:
            pc.delete_index(index_name)
            time.sleep(2)
            pc.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)

    return pc.Index(index_name)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into overlapping word-level chunks for embedding."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def upsert_paper(paper_id, paper_title, chunks, embedder, index,
                 batch_size=100, source_type="pdf"):
    """
    Upsert text chunks into Pinecone with metadata.
    source_type: 'pdf' or 'dataset' — stored in metadata for filtering.
    """
    vectors = embed_texts(chunks, embedder)
    records = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        records.append({
            "id": f"{paper_id}_chunk_{i}",
            "values": vector,
            "metadata": {
                "paper_id": paper_id,
                "paper_title": paper_title,
                "chunk_index": i,
                "text": chunk[:1000],
                "source_type": source_type,
            }
        })
    total = 0
    for i in range(0, len(records), batch_size):
        index.upsert(vectors=records[i:i+batch_size])
        total += len(records[i:i+batch_size])
    return total


def upsert_dataset(dataset_id, dataset_name, chunks, embedder, index,
                   batch_size=100):
    """Convenience wrapper to upsert dataset chunks with source_type='dataset'."""
    return upsert_paper(
        paper_id=dataset_id,
        paper_title=dataset_name,
        chunks=chunks,
        embedder=embedder,
        index=index,
        batch_size=batch_size,
        source_type="dataset",
    )


def semantic_search(query, embedder, index, top_k=5,
                    filter_paper_id=None, source_filter=None):
    """
    Search Pinecone for semantically similar chunks.
    source_filter: 'pdf', 'dataset', or None (both).
    """
    query_vector = embed_query(query, embedder)

    # Build filter dict from optional parameters
    filter_conditions = {}
    if filter_paper_id:
        filter_conditions["paper_id"] = {"$eq": filter_paper_id}
    if source_filter:
        filter_conditions["source_type"] = {"$eq": source_filter}

    filter_dict = filter_conditions if filter_conditions else None

    results = index.query(vector=query_vector, top_k=top_k,
                          include_metadata=True, filter=filter_dict)
    matches = []
    for match in results.matches:
        matches.append({
            "text": match.metadata.get("text", ""),
            "score": round(match.score, 4),
            "paper_title": match.metadata.get("paper_title", "Unknown"),
            "paper_id": match.metadata.get("paper_id", ""),
            "chunk_index": match.metadata.get("chunk_index", 0),
            "source_type": match.metadata.get("source_type", "pdf"),
        })
    return matches


def make_paper_id(filename: str) -> str:
    return hashlib.md5(filename.encode()).hexdigest()[:12]


def delete_paper(paper_id, index):
    try:
        results = index.query(vector=[0.0]*384, top_k=1000,
                              filter={"paper_id": {"$eq": paper_id}}, include_metadata=False)
        ids = [m.id for m in results.matches]
        if ids:
            index.delete(ids=ids)
        return len(ids)
    except Exception as e:
        print(f"[Delete error] {e}")
        return 0

import pytest

from src.rag_pipeline import chunk_text, embed_texts, get_embedder


def test_chunk_and_embed_basic():
    sample_text = "This is a small test. " * 200
    chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
    assert len(chunks) > 0

    embedder = get_embedder()
    vectors = embed_texts(chunks, embedder)

    assert len(vectors) == len(chunks)
    # Ensure vector dimensionality is 384 as expected for all-MiniLM-L6-v2
    assert len(vectors[0]) == 384

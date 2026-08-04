# 📚 InsightPaper AI — Research Paper Analysis Engine

> A RAG-Based System for Automated Research Paper Analysis Using Fine-Tuned Sentence Transformers, LLaMA 3.1, and Qwen 3.6.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square&logo=streamlit)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-green?style=flat-square)
![Qwen](https://img.shields.io/badge/Qwen%203.6-27B-blueviolet?style=flat-square)
![LLaMA](https://img.shields.io/badge/LLaMA%203.1-8B-orange?style=flat-square)
![RAG](https://img.shields.io/badge/RAG-Pipeline-purple?style=flat-square)

---

## 🧠 What is InsightPaper AI?

Most AI tools for research papers work at the surface level — summarizing abstracts or searching across databases of millions of papers.

**InsightPaper AI goes deeper.**

Upload any research paper PDF → it gets chunked, embedded using a fine-tuned Sentence-Transformer model, and indexed in Pinecone → you ask questions in natural language → top-5 relevant sections are retrieved → **Qwen 3.6 27B** or **LLaMA 3.1 8B** generates a precise, grounded answer with source citations.

---

## ✨ Key Features

- **Multi-Model LLM Selector** — choose between **Qwen 3.6 27B** (deep analytical reasoning) and **LLaMA 3.1 8B** (ultra-fast responses, ~420 ms)
- **Fine-Tuned Embedder** — fine-tuned `all-MiniLM-L6-v2` using MultipleNegativesRankingLoss (MNRL) on the Kaggle Summarized Research Papers dataset
- **LLM-as-a-Judge Evaluation** — automated 1–5 scoring of Faithfulness (zero-hallucination grounding), Relevance, and Completeness
- **PDF & Dataset Grounding** — supports PDF paper uploads and custom dataset indexing
- **Automated Summarisation** — structured summary cards (one-liner, problem, approach, key findings, limitations, keywords)
- **Source Citations** — every answer displays top-5 retrieved chunks with cosine similarity scores
- **Multimodal Figure Extraction** — automatically detects and extracts embedded images and links them with captions

---

## 🏗 RAG Architecture

```
PDF / Dataset Ingestion
    ↓
PyMuPDF — text & figure extraction
    ↓
Text Chunking — 500 words, 100-word sliding window overlap
    ↓
Fine-Tuned Embedder — models/fine_tuned_embedder (384-dim dense vectors)
    ↓
Pinecone Vector DB — serverless cosine similarity index with metadata filtering
    ↓
──────────────────────── Query Time ────────────────────────
User Question → fine-tuned embedder → Pinecone top-5 search
    ↓
Context Prompt Injection
    ↓
Selected LLM (Qwen 3.6 27B / LLaMA 3.1 8B) via Groq → grounded answer with citations
```

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Generative LLMs** | Qwen 3.6 27B (`qwen/qwen3.6-27b`) & LLaMA 3.1 8B (`llama-3.1-8b-instant`) via Groq API |
| **Embeddings** | Fine-Tuned Sentence-Transformers (`all-MiniLM-L6-v2` via MNRL loss) |
| **Vector Database** | Pinecone (Serverless, Cosine Similarity) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Evaluation Engine** | Token F1, Semantic Similarity, and LLM-as-a-Judge (Zheng et al., 2023) |
| **UI Framework** | Streamlit |
| **Environment** | Python 3.9+ |

---

## ⚡ Run Locally

### 1. Environment Setup
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the root directory:
```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Start the Web App
```bash
venv/bin/streamlit run app.py
```

### 4. Run Model Benchmark
```bash
PYTHONPATH=. venv/bin/python scripts/compare_models.py
```

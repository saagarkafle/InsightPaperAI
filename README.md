# 📚 InsightPaper AI — Research Paper Q&A Engine

> Ask anything about any research paper. Get answers grounded in the actual content — with exact source citations.

---

## 🧠 What is InsightPaper AI?

Most AI tools for research papers work at the surface level — summarizing abstracts or searching across databases of millions of papers.

**InsightPaper AI goes deeper.**

Upload any research paper PDF → text & figures are extracted → text is chunked, embedded using a fine-tuned Sentence-Transformer model, and stored in a Pinecone vector database → ask questions in natural language → top-5 relevant sections are retrieved → **Qwen 3.6 27B** or **LLaMA 3.1 8B** generates a precise, grounded answer with source citations.

---

## 📊 How InsightPaper AI Differs from Existing Tools

| Tool | What it does well | The gap |
|---|---|---|
| **Bohrium AI** | Searches 170M+ papers with citation-backed answers | Literature discovery tool — not designed for deep Q&A on your specific uploaded PDF |
| **Elicit AI** | Research question synthesis across thousands of papers | Works at abstract/metadata level, not section-level content |
| **Connected Papers** | Visualizes citation graphs to find related papers | Zero Q&A capability — discovery only, not comprehension |
| **SciSpace** | AI sidebar that explains highlighted text | Closed platform — no control over LLM, embeddings, or retrieval pipeline |
| **InsightPaper AI** | Deep Q&A on your specific uploaded paper | Full transparency — see exactly which chunks were retrieved, similarity scores, and model reasoning |

---

## ✨ Features

- **PDF Upload**: Drag and drop any research paper PDF; text & layout are extracted automatically.
- **Multi-Model LLM Selector**: Choose between **Qwen 3.6 27B** (deep analytical reasoning) and **LLaMA 3.1 8B** (fast Q&A).
- **Domain-Adapted Embeddings**: Fine-tuned `all-MiniLM-L6-v2` model trained with Multiple Negatives Ranking Loss (MNRL) on research datasets (falls back to base model if weights aren't local).
- **RAG Pipeline**: Retrieval-augmented generation targeting exact context, avoiding full-document hallucination.
- **Semantic Search Tab**: Search paper chunks directly by meaning and vector similarity rather than simple keyword matches.
- **Auto Paper Summary**: Automatically generates problem statements, approaches, key findings, keywords, and difficulty levels.
- **Source Citations**: Every answer displays top-5 retrieved chunks with cosine similarity scores.
- **Multimodal Figure Extraction**: Detects and extracts embedded figures/images linked with caption context.
- **RAG Stats Dashboard**: Visualizes RAG architecture, vector counts, and query metrics.
- **Token Efficient**: Sends only top-5 relevant chunks to the LLM instead of overloading the context window with the full paper.

---

## 🏗 RAG Architecture

```
PDF Upload
    ↓
PyMuPDF — text & figure extraction
    ↓
Text Chunking — 500 words, 100-word overlap
    ↓
Sentence Transformers — fine-tuned all-MiniLM-L6-v2 (384-dim embeddings)
    ↓
Pinecone — cosine similarity serverless vector index
    ↓
──────────────────────── Query Time ────────────────────────
User Question → embed query → Pinecone top-5 cosine search
    ↓
Retrieved top-5 chunks as context
    ↓
Selected LLM (Qwen 3.6 27B / LLaMA 3.1 8B) via Groq → grounded answer with citations
```

### Why RAG Instead of Sending the Full Paper?

| Approach | Token Usage | Accuracy | Works on Long Papers |
|---|---|---|---|
| **Full document in prompt** | Very High | Lower ("lost-in-the-middle" effect) | ❌ Exceeds token limits |
| **RAG (InsightPaper AI)** | Low (top-5 chunks) | Higher (focused context) | ✅ Any paper length |

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Generative LLMs** | Qwen 3.6 27B (`qwen/qwen3.6-27b`) & LLaMA 3.1 8B (`llama-3.1-8b-instant`) via Groq API |
| **Embeddings** | Fine-tuned `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Database** | Pinecone (Serverless, Cosine Similarity) |
| **PDF Parsing** | PyMuPDF (`fitz`) |
| **UI Framework** | Streamlit |
| **Environment** | Python 3.9+ |

---

## ⚡ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/saagarkafle/InsightPaperAI.git
cd InsightPaperAI
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the root directory:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Start the App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 🔑 Getting API Keys (Free)

| Key | Where to get it |
|---|---|
| **PINECONE_API_KEY** | [pinecone.io](https://pinecone.io) → Sign up → API Keys |
| **GROQ_API_KEY** | [console.groq.com](https://console.groq.com) → Create API Key |

*Note: Sentence Transformers runs locally — no API key needed for embeddings.*

---

## 📁 Project Structure

```
InsightPaperAI/
├── app.py                     # Streamlit entrypoint
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── data/                      # Benchmark & evaluation datasets
├── src/                       # Source codebase
│   ├── pdf_parser.py          # PDF text & image extraction
│   ├── rag_pipeline.py        # Embeddings + Pinecone vector index handlers
│   ├── llm_qa.py              # Groq LLM integration (Qwen/LLaMA) & summary generator
│   ├── evaluation.py         # RAG evaluation metrics
│   ├── mvc/                   # Model-View-Controller architecture
│   └── ui/                    # Streamlit tabs & visual components
├── scripts/                   # Evaluation & fine-tuning scripts
└── tests/                     # Pipeline unit tests
```

---

## 🖥 App Overview

- **Landing Page**: Drop your research paper PDF to begin processing.
- **Paper Dashboard**: Auto-generates structured summary, problem, approach, key findings, keywords, and difficulty level.
- **Ask Questions Tab**: Natural language Q&A with source citations and similarity scores.
- **Semantic Search Tab**: Direct vector similarity search across paper sections.
- **RAG Stats Tab**: Architecture visualization, vector counts, and session metrics.

---

## 📜 License

MIT License — free to use, modify, and build upon.

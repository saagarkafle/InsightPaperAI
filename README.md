# InsightPaper AI 📄

InsightPaper AI is an open-source RAG (Retrieval-Augmented Generation) engine designed to search, analyze, and query academic research papers in natural language.

Instead of reading through lengthy multi-page PDFs or relying on generic abstract summaries, InsightPaper AI parses your papers, splits them into semantic chunks, indexes them in Pinecone using a fine-tuned sentence-transformer model, and generates grounded answers with direct section citations using **Qwen 3.6 27B** or **LLaMA 3.1 8B** via Groq.

---

## Key Features

- **Multi-Model Reasoning**: Switch dynamically between **Qwen 3.6 27B** (for deep analytical responses) and **LLaMA 3.1 8B** (for rapid Q&A).
- **Domain-Adapted Embeddings**: Uses a fine-tuned `all-MiniLM-L6-v2` model trained with Multiple Negatives Ranking Loss (MNRL) on research datasets. Automatically falls back to the base model if custom local weights aren't present.
- **Fast Vector Search**: Built on Pinecone Serverless vector storage for fast cosine similarity retrieval.
- **Source Citations**: Displays top retrieved text chunks alongside similarity scores so you can verify answers directly against the source paper.
- **Structured Paper Summaries**: Generates one-line overviews, problem statements, core methodologies, key findings, and limitations.
- **PDF & Figure Parsing**: Extracts text layout and embedded images/figures using PyMuPDF.
- **Evaluation Benchmark**: Includes built-in evaluation tools using Token F1, semantic similarity, and LLM-as-a-Judge scoring.

---

## How It Works

```
[ Upload PDF / Dataset ]
          │
          ▼
[ PyMuPDF Text & Figure Extraction ]
          │
          ▼
[ 500-Word Overlapping Chunks ]
          │
          ▼
[ Sentence Transformer Embedder ]
          │
          ▼
[ Pinecone Vector Indexing ]
          │
          ▼
┌──────────────────────────────────────────────┐
│ User Question                                │
│   └─► Embedding & Top-5 Cosine Search        │
│   └─► Context Injection into Prompt          │
│   └─► Inference via Groq (Qwen / LLaMA 3.1)  │
│   └─► Answer with Source Citations           │
└──────────────────────────────────────────────┘
```

---

## Tech Stack

- **Frontend**: Streamlit
- **LLM Inference**: Groq API (`qwen/qwen3.6-27b`, `llama-3.1-8b-instant`)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Vector Database**: Pinecone (Serverless)
- **PDF Extraction**: PyMuPDF (`fitz`)
- **Evaluation**: Custom evaluation scripts for Token F1, Cosine Similarity, and LLM-as-a-Judge

---

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/saagarkafle/InsightPaperAI.git
cd InsightPaperAI
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add API Keys
Create a `.env` file in the root directory:
```env
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Web App
```bash
streamlit run app.py
```

---

## Running Benchmarks & Evaluation

You can run the included scripts to benchmark model accuracy and retrieval performance:

```bash
# Run pipeline evaluation against test datasets
PYTHONPATH=. python scripts/evaluate_pipeline.py

# Compare performance between Qwen and LLaMA models
PYTHONPATH=. python scripts/compare_models.py
```

---

## Free Cloud Deployment

This app can be hosted for free on **Streamlit Community Cloud**:

1. Push your repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Select this repository and set `app.py` as the main entry point.
4. Go to **Advanced Settings -> Secrets** and paste your environment variables:
   ```toml
   PINECONE_API_KEY = "your_pinecone_api_key"
   GROQ_API_KEY = "your_groq_api_key"
   ```
5. Click **Deploy**.

---

## Project Structure

```
InsightPaperAI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python package requirements
├── README.md               # Project documentation
├── data/                   # Benchmark datasets (JSONL format)
├── src/                    # Core application logic
│   ├── pdf_parser.py       # PDF layout and figure parsing
│   ├── rag_pipeline.py     # Embedding generation and Pinecone integration
│   ├── llm_qa.py           # Groq LLM inference handlers
│   ├── evaluation.py      # Metric calculations (Token F1, LLM-as-a-Judge)
│   ├── mvc/                # Controller and View structure for Streamlit
│   └── ui/                 # UI components and layout styling
└── scripts/                # Evaluation & model fine-tuning scripts
```


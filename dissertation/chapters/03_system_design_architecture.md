\chapter{System Design and Architecture}

\section{Introduction}

This chapter presents the complete system design of InsightPaper AI, covering the software development methodology, requirements specification, architectural design, technology stack, and pipeline design for each major component. The chapter moves from high-level design decisions down to the specific schemas and configurations that define how the system behaves. All design decisions documented here form the direct blueprint realised in Chapter 4.

\section{Development Methodology and SDLC Model}

\subsection{Chosen Methodology}

The development of InsightPaper AI followed an Iterative Prototyping model, which combines elements of Agile iteration with structured Waterfall milestones. This hybrid approach was selected because the project involves tightly coupled components — a retrieval pipeline, a fine-tuned embedding model, generative LLM integration, and an interactive web interface — each of which required continuous evaluation and refinement throughout development.

  A pure sequential Waterfall model would have been inappropriate for an AI-driven RAG system for several reasons. Retrieval-Augmented Generation pipelines are inherently data-dependent: the quality of the embedding model, the chunking window size, and the prompt engineering strategy cannot be defined precisely in advance. They must instead be experimentally validated through iterative cycles of testing, measurement, and refinement. For instance, the initial baseline embedding model (all-MiniLM-L6-v2) achieved a Retrieval Recall@5 of only 23.3\%, which was only discovered after implementation and empirical evaluation. This finding necessitated a domain-specific fine-tuning phase that was planned as an iterative research loop rather than a fixed upfront deliverable.

  The adopted SDLC progressed through five sequential phases, each producing concrete artefacts before the next began.

\begin{itemize}

\item Phase 1 — Requirements and Research (Weeks 1–2): Literature review, technology selection, and functional and non-functional requirements specification.

\item Phase 2 — Data Engineering and Preprocessing (Week 2): Kaggle dataset ingestion, chunking strategy design, and anchor-positive pair generation for contrastive training.

\item Phase 3 — System Architecture and Pipeline Design (Weeks 2–3): MVC architectural design, RAG pipeline module specification, and Pinecone index schema definition.

\item Phase 4 — Iterative Implementation and Fine-Tuning (Weeks 3–4): Incremental Streamlit prototype development, PDF parsing integration, vector indexing, Groq API middleware, and embedding model fine-tuning execution.

\item Phase 5 — Evaluation and Benchmarking (Week 5): Corpus-wide retrieval benchmarking, LLM comparative evaluation, and latency profiling.

\end{itemize}

Below as shown in Figure \ref{fig:sdlc} is a diagram illustrating the iterative SDLC roadmap adopted for the development of InsightPaper AI.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.1.png}

\caption{SDLC Iterative Prototyping Roadmap for InsightPaper AI}

\label{fig:sdlc}

\end{figure}

Below as shown in Table \ref{tab:phases} is a summary of each development phase, its key activities, primary deliverable, and duration.

\begin{table}[H][H]

\centering

\caption{Development Phase Summary}

\label{tab:phases}

\begin{tabular}{|p{3.5cm}|p{4cm}|p{3.5cm}|p{2cm}|}

\hline

\textbf{Phase} & \textbf{Activities} & \textbf{Key Deliverable} & \textbf{Duration} \\

\hline

1. Requirements \& Research & Literature review, requirements elicitation & Requirements specification & Week 1–2 \\

\hline

2. Data Engineering & Kaggle dataset preprocessing, pair generation & kaggle\_train.jsonl, kaggle\_eval.jsonl & Week 2 \\

\hline

3. Architecture Design & MVC design, pipeline specification, schema design & Architecture diagrams & Week 2–3 \\

\hline

4. Implementation \& Fine-Tuning & Streamlit UI, PDF parsing, RAG pipeline, fine-tuning & Functional web app, fine\_tuned\_embedder/ & Week 3–4 \\

\hline

5. Evaluation \& Benchmarking & Retrieval benchmarking, LLM comparison, latency tests & Benchmark results report & Week 5 \\

\hline

\end{tabular}

\end{table}

\section{Requirements Analysis and Use Case Modelling}

\subsection{Functional Requirements}

The functional requirements were derived from the primary research objective: to build an end-to-end RAG system capable of answering natural language queries about scientific research papers with zero hallucination. The system must support both individual researchers and evaluators. Table \ref{tab:fr} presents the complete set of functional requirements.

\begin{table}[H][H]

\centering

\caption{Functional Requirements Specification}

\label{tab:fr}

\begin{tabular}{|p{1.2cm}|p{9cm}|p{2cm}|}

\hline

\textbf{ID} & \textbf{Requirement} & \textbf{Priority} \\

\hline

FR-01 & The system shall accept PDF research papers as input via a web interface & High \\

\hline

FR-02 & The system shall extract and clean all text content and figures from uploaded PDFs & High \\

\hline

FR-03 & The system shall split extracted text into overlapping semantic chunks and index them into a vector database & High \\

\hline

FR-04 & The system shall support natural language question-answering grounded strictly in retrieved paper content & High \\

\hline

FR-05 & The system shall provide a model selector allowing the user to switch between Qwen 3.6 27B and LLaMA 3.1 8B & Medium \\

\hline

FR-06 & The system shall automatically generate a structured summary of the uploaded paper & Medium \\

\hline

FR-07 & The system shall accept CSV/JSON evaluation datasets and compute Token F1, Semantic Similarity, and LLM-as-a-Judge scores & Medium \\

\hline

FR-08 & The system shall persist session state across browser re-renders without re-processing documents & Low \\

\hline

\end{tabular}

\end{table}

\subsection{Non-Functional Requirements}

Table \ref{tab:nfr} presents the non-functional requirements governing the performance, security, and reliability of the system.

\begin{table}[H][H]

\centering

\caption{Non-Functional Requirements Specification}

\label{tab:nfr}

\begin{tabular}{|p{1.2cm}|p{8cm}|p{3.5cm}|}

\hline

\textbf{ID} & \textbf{Requirement} & \textbf{Target} \\

\hline

NFR-01 & Retrieval latency per query shall be minimal & Under 500ms for vector search \\

\hline

NFR-02 & Generated answers shall be grounded solely in retrieved content & 5.00/5.00 Faithfulness score \\

\hline

NFR-03 & The system shall handle multi-page academic PDFs reliably & Tested on 50+ page documents \\

\hline

NFR-04 & The system shall be deployable locally via a Python virtual environment & venv/bin/streamlit run app.py \\

\hline

NFR-05 & API credentials shall be stored securely and never hardcoded & .env file configuration \\

\hline

\end{tabular}

\end{table}

\subsection{UML Use Case Diagram}

The primary actor in the system is the Academic Researcher or Student, who interacts with InsightPaper AI through a browser-based Streamlit interface. A secondary actor — the Evaluator or Administrator — uses the dataset upload and evaluation module to run quantitative benchmarks. Below as shown in Figure \ref{fig:usecase} is the UML Use Case Diagram for InsightPaper AI.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.2.png}

\caption{UML Use Case Diagram for InsightPaper AI}

\label{fig:usecase}

\end{figure}

Table \ref{tab:usecases} describes each identified use case, its primary actor, and its purpose.

\begin{table}[H][H]

\centering

\caption{Use Case Descriptions}

\label{tab:usecases}

\begin{tabular}{|p{1.2cm}|p{4cm}|p{2.5cm}|p{5cm}|}

\hline

\textbf{ID} & \textbf{Use Case} & \textbf{Actor} & \textbf{Description} \\

\hline

UC-01 & Upload PDF Research Paper & Researcher & Upload a PDF; system parses, chunks, and indexes it into Pinecone \\

\hline

UC-02 & Select LLM Model & Researcher & Choose Qwen 3.6 27B or LLaMA 3.1 8B from a dropdown \\

\hline

UC-03 & View Paper Summary & Researcher & View auto-generated structured summary including problem, method, findings, and keywords \\

\hline

UC-04 & Submit Natural Language Query & Researcher & Ask a question; system retrieves top-5 chunks and returns a grounded answer \\

\hline

UC-05 & Browse Extracted Figures & Researcher & View figures detected in the paper with auto-matched captions and page references \\

\hline

UC-06 & Upload Evaluation Dataset & Evaluator & Upload a CSV or JSON file with ground-truth question-answer pairs \\

\hline

UC-07 & Run Benchmark Evaluation & Evaluator & Trigger automated scoring across Token F1, Semantic Similarity, and LLM-as-a-Judge \\

\hline

\end{tabular}

\end{table}

\section{Overall System Architecture}

\subsection{High-Level MVC Architecture}

InsightPaper AI is structured following the Model-View-Controller (MVC) architectural design pattern. This separation of concerns ensures that data logic, presentation logic, and orchestration logic remain independently modifiable, reducing coupling and improving maintainability across the codebase.

  The View layer contains all user interface components encapsulated in src/ui/, including the landing page, navbar, dashboard tabs, and footer. These are rendered by Streamlit. The View never accesses data directly; it delegates all user interaction events to the Controller.

  The Controller layer, implemented in src/mvc/controller.py, is the central orchestrator. It determines application state — whether to render the upload landing page or the main dashboard — routes user interactions to appropriate model methods, and handles model selection and session restoration events.

  The Model layer, implemented in src/mvc/model.py, contains all business logic: PDF parsing, text chunking, vector indexing via Pinecone, LLM inference via Groq, session state persistence, and evaluation metrics computation. The application entry point is app.py, a twelve-line file responsible solely for initialising the Streamlit browser tab configuration and instantiating the AppController.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.3.png}

\caption{High-Level MVC System Architecture of InsightPaper AI}

\label{fig:mvc}

\end{figure}

\subsection{RAG Query Processing Sequence}

The following sequence describes the complete processing lifecycle when a researcher submits a natural language question through the interface.

\begin{itemize}

\item The Researcher types a query into the Streamlit chat input field.

\item The AppController captures the submission event and delegates to AppModel.answer\_question().

\item The RAG Pipeline in src/rag\_pipeline.py encodes the query into a 384-dimensional dense vector using the fine-tuned SentenceTransformer embedder loaded from models/fine\_tuned\_embedder/.

\item The Pinecone Client receives the query vector and performs cosine similarity search, returning the top-5 most semantically relevant chunk vectors and their metadata including text, page number, and paper ID.

\item The Prompt Builder assembles the five retrieved context chunks into a strict system prompt instructing the LLM to answer solely from the provided content and never from its training data.

\item The Groq API Client in src/llm\_qa.py dispatches the constructed prompt to the user-selected LLM. For Qwen 3.6, internal think reasoning tokens are stripped via regex parsing before the answer is returned.

\item The AppView renders the grounded answer in the chat interface and optionally surfaces source chunk citations in an expandable reference panel.

\end{itemize}

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.4.png}

\caption{UML Sequence Diagram — RAG Query Processing Pipeline}

\label{fig:sequence}

\end{figure}

\section{Technology Stack Justification}

The selection of each technology was guided by trade-off analysis across inference speed, memory efficiency, retrieval accuracy, developer productivity, and cost. The full stack was validated on a local Python 3.13 virtual environment. Table \ref{tab:stack} presents the complete technology stack with justifications.

\begin{table}[H][H]

\centering

\caption{InsightPaper AI Technology Stack}

\label{tab:stack}

\begin{tabular}{|p{2.5cm}|p{2.5cm}|p{1.5cm}|p{6cm}|}

\hline

\textbf{Layer} & \textbf{Technology} & \textbf{Version} & \textbf{Justification} \\

\hline

Web Framework & Streamlit & 1.35.0+ & Native Python web rendering with built-in session state. Enables rapid prototyping of data-heavy interactive UIs without JavaScript. \\

\hline

PDF Parsing & PyMuPDF (fitz) & 1.24.0+ & C-accelerated PDF processing providing robust text block extraction, figure detection, and caption heuristic matching. \\

\hline

Embedder & SentenceTransformers & 2.2.0+ & Industry-standard library for dense sentence embedding. all-MiniLM-L6-v2 (384-d) offers strong semantic quality at minimal inference overhead. \\

\hline

Vector Database & Pinecone & 3.0.0+ & Serverless cloud-native HNSW vector store with cosine similarity indexing and sub-50ms retrieval at scale. \\

\hline

LLM Inference & Groq API & OpenAI-compatible & LPU-accelerated inference delivering 800+ tokens per second, significantly outperforming standard GPU-based APIs for real-time QA. \\

\hline

Primary LLM & Qwen 3.6 27B & qwen3.6-27b & 27-billion parameter model. Selected as default for Qwen 3.6 27B (Deep Analysis) for complex queries and 300–500 word executive summaries. \\

\hline

Secondary LLM & LLaMA 3.1 8B & llama-3.1-8b-instant & Lightweight 8B model. Selected for LLaMA 3.1 8B (Fast Inference) delivering ~400ms average latency for rapid iterative Q\&A. \\

\hline

Evaluation & Custom evaluation.py & — & Token F1, Semantic Similarity, and LLM-as-a-Judge implemented natively in src/evaluation.py. \\

\hline

\end{tabular}

\end{table}

\section{Core RAG Pipeline Design}

\subsection{PDF Parsing and Text Extraction}

The PDF ingestion pipeline in src/pdf\_parser.py uses PyMuPDF to process each page of the uploaded document sequentially. Raw text is extracted as character sequences per page and normalised by collapsing excessive whitespace and redundant blank line sequences. A parallel figure extraction pass scans each page for embedded image objects and applies a caption-matching heuristic: if text immediately adjacent to an image matches the pattern Figure N or Fig. N, the caption is captured and associated with the base64-encoded image data and its page number. The pipeline returns three artefacts: the complete normalised plain-text body, a list of detected figure objects, and document-level metadata including word count and page count.

\subsection{Text Chunking Strategy Design}

Due to context window constraints of transformer-based embedding models, full paper text cannot be encoded as a single vector. The system implements a sliding-window overlapping chunking strategy, dividing text into fixed-size segments with a controlled overlap to prevent semantic information from being severed at chunk boundaries. Table \ref{tab:chunking} presents the configuration parameters.

\begin{table}[H][H]

\centering

\caption{Text Chunking Configuration}

\label{tab:chunking}

\begin{tabular}{|p{3.5cm}|p{2.5cm}|p{7cm}|}

\hline

\textbf{Parameter} & \textbf{Value} & \textbf{Rationale} \\

\hline

Chunk Size & 500 words & Aligned with the effective semantic context range of all-MiniLM-L6-v2 without truncation \\

\hline

Chunk Overlap & 100 words (20\%) & Ensures sentences straddling chunk boundaries appear in both adjacent chunks \\

\hline

Primary Separator & Paragraph breaks & Respects structural paragraph divisions in academic text \\

\hline

Fallback Separator & Sentence endings & Applied when paragraphs exceed the chunk size threshold \\

\hline

\end{tabular}

\end{table}

A typical 8,000-word research paper generates approximately 20 to 30 chunks under this configuration. Below as shown in Figure \ref{fig:chunking} is a diagram illustrating the overlapping sliding-window chunking mechanism.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.5.png}

\caption{Overlapping Sliding-Window Chunking Mechanism}

\label{fig:chunking}

\end{figure}

\section{Vector Index and Database Schema Design}

Each produced text chunk is encoded by the fine-tuned SentenceTransformer embedder into a 384-dimensional dense floating-point vector. These vectors, together with associated metadata, are upserted into a Pinecone Serverless index configured with cosine similarity as the distance metric. The Pinecone index schema supports multi-document session isolation through per-paper namespacing and enables efficient metadata-filtered retrieval. Table \ref{tab:pinecone} presents the complete schema.

\begin{table}[H][H]

\centering

\caption{Pinecone Vector Index Metadata Schema}

\label{tab:pinecone}

\begin{tabular}{|p{3cm}|p{2.5cm}|p{7cm}|}

\hline

\textbf{Field} & \textbf{Data Type} & \textbf{Description} \\

\hline

id & String & Unique identifier: SHA-256 hash of paper\_id and chunk\_index \\

\hline

values & Float[384] & Dense embedding vector from the fine-tuned SentenceTransformer \\

\hline

metadata.text & String & Raw chunk text; injected directly as context into the RAG prompt \\

\hline

metadata.page & Integer & Source page number; displayed as an inline citation in the UI \\

\hline

metadata.paper\_id & String & UUID of the parent document; used for namespace isolation \\

\hline

metadata.chunk\_index & Integer & Sequential chunk position within the document \\

\hline

metadata.source\_type & String & Either pdf or dataset, enabling source-type-filtered retrieval \\

\hline

\end{tabular}

\end{table}

At query time, the user question is embedded into the same 384-dimensional space and a top-K cosine similarity search is executed against the active paper's Pinecone namespace with K set to 5. Below as shown in Figure \ref{fig:indexing} is the vector embedding and indexing pipeline.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/3.6.png}

\caption{Vector Embedding and Pinecone Indexing Pipeline}

\label{fig:indexing}

\end{figure}

\section{Evaluation Framework Design Specifications}

The evaluation framework in src/evaluation.py measures generated answer quality across three complementary dimensions, addressing the known limitations of single-metric assessment in QA evaluation. Table \ref{tab:metrics} presents the metrics matrix.

\begin{table}[H][H]

\centering

\caption{Evaluation Metrics Design Matrix}

\label{tab:metrics}

\begin{tabular}{|p{3cm}|p{2cm}|p{4cm}|p{4cm}|}

\hline

\textbf{Metric} & \textbf{Type} & \textbf{What It Measures} & \textbf{Method} \\

\hline

Token-Level F1 Score & Lexical & Exact token overlap between generated and ground-truth answers & F1 = 2 x (Precision x Recall) / (Precision + Recall) at token level \\

\hline

Semantic Vector Similarity & Semantic & Conceptual alignment regardless of vocabulary choice & Cosine similarity between 384-d embeddings of generated and reference answers \\

\hline

LLM-as-a-Judge (Zheng et al., 2023) & Holistic & Faithfulness, Relevance, and Completeness rated 1–5 & Evaluator LLM judges generated answer against retrieved source context \\

\hline

\end{tabular}

\end{table}

Token F1 penalises semantically correct but paraphrased answers. Semantic Similarity addresses this by measuring meaning-level alignment. LLM-as-a-Judge captures subjective qualitative properties such as explanation depth and completeness that neither lexical nor embedding-based metrics can quantify.

\section{Chapter Summary}

This chapter presented the complete system design of InsightPaper AI. An iterative SDLC methodology was selected to accommodate the empirical nature of RAG pipeline tuning. A formal requirements specification covering eight functional and five non-functional requirements was produced alongside a UML use case model. The MVC architectural pattern was adopted to ensure clean separation of UI, orchestration, and data logic. Each technology was justified through explicit trade-off analysis. The PDF parsing pipeline, overlapping chunking strategy, Pinecone vector schema, and three-dimensional evaluation framework were all specified in design terms. These design decisions are realised in code and demonstrated through prototypes in Chapter 4.

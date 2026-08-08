
\chapter{System Implementation and Prototypes}

\section{Introduction}
This chapter describes the practical realisation of InsightPaper AI across all system components. It moves from high-level architectural decisions established in Chapter 3 to specific code integration, API middleware, and the functional web interface prototypes. Three annotated UI prototypes are presented, followed by the session state management strategy and dataset evaluation pipeline.

\section{System Integration and Component Realisation}

\subsection{Application Entry Point and MVC Instantiation}
The application is launched via app.py, a deliberately minimal file that configures the Streamlit browser tab metadata and instantiates the AppController. This design decision ensures the entry point remains decoupled from all business logic, keeping the controller as the sole orchestration boundary. The file contains only twelve lines of code, setting the page title to InsightPaper AI, the page icon, and the layout to wide before handing control entirely to the controller.
\newline \newline The AppController.run() method checks st.session\_state for an active processed paper. If no paper is loaded, the landing page view is rendered. If a paper session exists, the main dashboard is rendered with the appropriate tabs.

\subsection{PDF Parsing Pipeline Implementation}
The PDF parsing module in src/pdf\_parser.py uses PyMuPDF to process each uploaded document. The parsing function opens the document, iterates page by page, extracts text blocks, and normalises whitespace. Concurrently, a figure detection pass identifies embedded image objects and applies caption matching using regular expression patterns for common academic figure labels such as Figure, Fig., and FIGURE.
\newline \newline The parser returns a structured ParsedDocument dataclass containing three fields: full\_text as a normalised concatenated string, figures as a list of FigureObject instances each containing image bytes, matched caption, and page number, and metadata as a DocumentMetadata object containing word count, page count, and estimated difficulty level.

\subsection{RAG Pipeline and Pinecone Integration}
The RAG pipeline in src/rag\_pipeline.py handles both the indexing phase at upload time and the retrieval phase at query time.
\newline \newline During indexing, text chunks are produced by the sliding-window chunker and passed individually to the SentenceTransformer embedder. The resulting 384-dimensional vectors are batched and upserted into Pinecone alongside their metadata payloads. Pinecone connections are established using the PINECONE\_API\_KEY loaded via python-dotenv from the .env file.
\newline \newline During retrieval, the query string is encoded by the same embedder and submitted to Pinecone's query API with top\_k set to 5 and a filter clause scoped to the active paper\_id namespace. The returned matches contain both the vector score and the associated metadata.text and metadata.page fields used for citation display.

\subsection{Groq API Middleware and LLM Routing}
LLM inference is handled in src/llm\_qa.py, which uses the openai Python SDK configured against Groq's OpenAI-compatible endpoint at https://api.groq.com/openai/v1. The model identifier is passed dynamically based on the user's selection stored in st.session\_state.selected\_model.
\newline \newline A critical implementation detail for Qwen 3.6 27B is the removal of think chain-of-thought reasoning blocks from the raw response using a compiled regular expression pattern, ensuring only the final cleaned answer is displayed to the user.
\newline \newline A safety fallback mechanism was implemented for the paper summarisation feature: if Qwen 3.6 27B raises a token-limit exception during summarisation of unusually long papers, the system automatically retries the request using LLaMA 3.1 8B, preventing the summary panel from returning an empty or error state.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/4.1.png}
  \caption{Groq API Middleware and Model Routing Architecture}
  \label{fig:routing}
\end{figure}

\section{Prototype Implementation and Web UI Screenshots}
The following subsections present annotated screenshots of each major interface prototype. All prototypes were implemented in Streamlit with a custom CSS stylesheet injected via src/ui/css.py and Google Fonts for typographic consistency.

\subsection{Prototype 1: Document Upload and Model Selection Interface}
The landing page is the first screen presented to users upon launching InsightPaper AI. It features a clean centred layout with the application logo, an AI Model Selection dropdown, and a PDF file uploader. The model selection dropdown defaults to Qwen 3.6 27B and allows the user to switch to LLaMA 3.1 8B before processing begins.
\newline \newline Upon selecting a PDF and clicking Process Paper, a progress spinner is displayed while the parsing, chunking, embedding, and Pinecone indexing pipeline runs. A status message confirms successful indexing before the dashboard is rendered. Below as shown in Figure \ref{fig:proto1} is the landing page interface.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/4.2.png}
  \caption{Prototype 1 — Landing Page: PDF Upload and AI Model Selection Interface}
  \label{fig:proto1}
\end{figure}

The key components visible in this interface are: the AI Model Selection dropdown offering Qwen 3.6 27B and LLaMA 3.1 8B, the PDF file uploader with drag-and-drop support, the Process Paper action button, and the processing progress spinner showing step-by-step status messages as each pipeline stage completes.

\subsection{Prototype 2: Main Dashboard and Interactive Q\&A Interface}
After successful processing, the application transitions to the main dashboard. The layout follows a three-column structure: a left panel with navigation tabs for Ask Questions, Figures, Search, and Stats, a central panel displaying the paper title and structured summary cards, and a right sidebar for model toggling and source type switching.
\newline \newline The Ask Questions tab contains the core RAG question-answering interface. A chat input field accepts natural language queries, and responses are rendered in a scrollable chat thread. Each AI response optionally includes an expandable Source Citations section displaying the exact retrieved chunks from Pinecone, including their source page numbers, providing full transparency on the grounding of each answer. Below as shown in Figure \ref{fig:proto2} is the main dashboard Q\&A interface.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/4.3.png}
  \caption{Prototype 2 — Main Dashboard: RAG Question-Answering Interface with Source Citations}
  \label{fig:proto2}
\end{figure}

The key components visible in this interface are: the structured paper summary cards showing problem, method, findings, and keywords; the navigation tabs for different dashboard sections; the chat input field for natural language queries; the LLM-generated grounded answer; the expandable source citations panel showing chunk text and page number; and the sidebar model switcher allowing active session model toggling.

\subsection{Prototype 3: Automated Evaluation and Metric Visualiser}
When an evaluation dataset in CSV or JSON format containing question and answer columns is uploaded alongside a PDF, a dedicated Evaluate tab becomes active on the dashboard. This tab presents the automated quantitative benchmarking interface.
\newline \newline The user triggers evaluation with a single button click. The system iterates through each Q\&A pair in the dataset, submits each question through the full RAG pipeline, and computes Token F1, Semantic Similarity, and LLM-as-a-Judge scores for each generated answer. Results are displayed in a results table alongside aggregate averages. Below as shown in Figure \ref{fig:proto3} is the evaluation dashboard interface.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/4.4.png}
  \caption{Prototype 3 — Evaluation Dashboard: Automated Benchmark Scoring Interface}
  \label{fig:proto3}
\end{figure}

The key components visible in this interface are: the dataset upload panel for CSV or JSON files; the Run Evaluation action button; the per-question results table showing Token F1, Semantic Similarity, and LLM Judge score for each entry; the aggregate average scores panel; and the LLM-as-a-Judge individual verdict display showing Faithfulness, Relevance, and Completeness ratings.

\section{Session Management and State Persistence}

\subsection{In-Session State with Streamlit Session State}
Streamlit re-renders the entire Python script on every user interaction by design. Without explicit state management, this would force a full re-parse and re-index of the PDF on every button press or query submission, an operation taking several seconds per document.
\newline \newline InsightPaper AI manages this through st.session\_state, a dictionary-like object persisted across re-renders within the same browser session. All expensive pipeline outputs are stored in session state after the first computation and retrieved from it on subsequent renders. Table \ref{tab:state} presents the complete session state schema.

\begin{table}[h]
\centering
\caption{Streamlit Session State Key Schema}
\label{tab:state}
\begin{tabular}{|p{3.5cm}|p{2.5cm}|p{7cm}|}
\hline
\textbf{State Key} & \textbf{Data Type} & \textbf{Purpose} \\
\hline
processed\_paper\_id & String & UUID of the currently active indexed document \\
\hline
paper\_metadata & Dict & Cached word count, page count, and title \\
\hline
paper\_summary & Dict & Cached structured summary including problem, method, findings, and keywords \\
\hline
chat\_history & List[Dict] & Full multi-turn conversation history with role and content per message \\
\hline
selected\_model & String & Currently active LLM model identifier \\
\hline
figures & List[FigureObject] & Extracted figures and captions from the current paper \\
\hline
source\_type & String & Active source: either pdf or dataset \\
\hline
dataset\_metadata & Dict & Dataset row count and column schema if a dataset is loaded \\
\hline
\end{tabular}
\end{table}

\subsection{Cross-Session Persistence with State File}
Beyond the browser session, InsightPaper AI persists indexed paper metadata to a local JSON file named .insightpaper\_state.json managed by src/state.py. This enables the application to restore the last active paper session automatically when the app is restarted, without requiring re-upload or re-indexing. The state file records the list of previously indexed paper IDs and their associated metadata, allowing users to switch between multiple indexed papers within a single session.

\section{Dataset Upload and Evaluation Module}

\subsection{Dataset Ingestion}
The evaluation module in src/evaluation.py accepts datasets in two formats: CSV parsed using Python's built-in csv module, and JSON parsed as an array of objects. Upon upload, the system validates that the required question and answer columns are present. An optional context column, if provided, is stored alongside each pair for reference.
\newline \newline After validation, the dataset text content is extracted and indexed into Pinecone under a dataset source namespace, enabling semantic search over dataset content separately from the PDF body.

\subsection{Automated Scoring Pipeline}
The evaluation pipeline iterates over all Q\&A pairs and for each entry completes the following sequence.

\begin{itemize}
\item The question is submitted to the full RAG pipeline, producing a generated answer grounded in Pinecone-retrieved context.
\item Token-Level F1 is computed between the generated and reference answers using shared token overlap.
\item Both answers are encoded via the SentenceTransformer embedder and cosine similarity is computed between their 384-dimensional vectors.
\item A structured judge prompt is submitted to the active LLM requesting a 1 to 5 rating across Faithfulness, Relevance, and Completeness dimensions.
\end{itemize}

Results are aggregated into a summary table and displayed in the Evaluate tab dashboard. Below as shown in Figure \ref{fig:evalarch} is the automated benchmark scoring pipeline architecture.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/4.5.png}
  \caption{Automated Benchmark Scoring Pipeline Architecture}
  \label{fig:evalarch}
\end{figure}

\section{Chapter Summary}
This chapter presented the practical implementation of InsightPaper AI across all system components. The MVC codebase structure was demonstrated through key module implementations including the Groq API model router, Pinecone RAG pipeline, and Streamlit session state manager. Three annotated UI prototype screenshots illustrated the Document Upload interface in Prototype 1, the interactive RAG Question-Answering dashboard in Prototype 2, and the automated Evaluation module in Prototype 3. The dataset evaluation pipeline and cross-session state persistence mechanisms were also detailed. Chapter 5 addresses the critical research contribution of this project: the domain-specific fine-tuning of the SentenceTransformer embedding model.

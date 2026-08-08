
\chapter{System Implementation and Prototypes}

\section{Introduction}
This chapter describes the practical realisation of InsightPaper AI across all system components. It moves from high-level architectural decisions established in Chapter 3 to specific code integration, API middleware, and the functional web interface prototypes. Four annotated UI prototypes are presented, followed by the session state management strategy and dataset evaluation pipeline.

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
\newline \newline A token payload safeguard was implemented to prevent Groq API rate-limit exceptions: prompt text excerpts for summary generation are bounded to 1,800 words and completion max\_tokens set to 1,000, requesting ~3,300 tokens per call and remaining strictly beneath Groq's 6,000 Tokens Per Minute (TPM) limit. Additionally, a safety fallback mechanism automatically retries requests using LLaMA 3.1 8B if primary LLM calls fail.

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.1.png}
  \caption{Groq API Middleware and Model Routing Architecture}
  \label{fig:routing}
\end{figure}

\section{Prototype Implementation and Web UI Screenshots}
The following subsections present annotated screenshots of each major interface prototype. All prototypes were implemented in Streamlit with a custom CSS stylesheet injected via src/ui/css.py, featuring a Spotify-inspired Dark Theme design system (\#121212 dark background, \#181818 card containers, \#242424 section cards, and \#1DB954 Spotify Green accent pill buttons and highlight tags).

\subsection{Prototype 1: Document Upload and Model Selection Interface}
The landing page is the first screen presented to users upon launching InsightPaper AI. It features a clean centred layout with the application logo, an AI Model Selection dropdown, a unified PDF dropzone card, and an automated step-by-step workflow guide. The model selector offers two clear options: Qwen 3.6 27B (Deep Analysis) for complex queries and LLaMA 3.1 8B (Fast Inference) for rapid iterative Q\&A, paired with a dynamic hint card explaining when to choose each model.
\newline \newline When a PDF is selected, an instant file upload confirmation badge displays the file name, size in MB, and a green readiness state. Upon clicking Process Paper, a bidirectional JavaScript smooth-scroll script automatically scrolls the viewport down to the live status widget (st.status) showing parsing, chunking, embedding, and indexing progress, before smoothly auto-scrolling back to top: 0 when the dashboard renders. Below as shown in Figure \ref{fig:proto1} is the landing page interface.

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.2.png}
  \caption{Prototype 1 — Landing Page: PDF Upload and AI Model Selection Interface}
  \label{fig:proto1}
\end{figure}

The key components visible in this interface are: the AI Model Selection dropdown offering Qwen 3.6 27B (Deep Analysis) and LLaMA 3.1 8B (Fast Inference); the dynamic model selection guide hint; the unified PDF file uploader with instant file confirmation badge; the Process Paper action button; and the automated 6-step pipeline workflow panel.

\subsection{Prototype 2: Main Dashboard with Summary}
After successful processing, the application transitions to the main dashboard. The central panel presents the primary document summary overview: paper title, difficulty rating, field tag, problem statement, approach, and key findings.
\newline \newline The overview card includes a dedicated Read Elaborated Summary (300–500 words) button, allowing users to launch an in-depth modal dialog. Below as shown in Figure \ref{fig:proto2} is the main dashboard summary interface.

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.3.png}
  \caption{Prototype 2 — Main Dashboard: Paper Overview and Structured Summary Interface}
  \label{fig:proto2}
\end{figure}

The key components visible in this interface are: the structured paper summary overview card; the Read Elaborated Summary modal trigger button; the key findings list; the topic tags panel; the vertical navigation tabbar; and the right sidebar model selector.

\subsection{Prototype 3: Q\&A Interface}
The Ask Questions tab contains the core interactive Retrieval-Augmented Generation question-answering interface. It allows users to ask natural language questions about the indexed paper and receive precise, grounded answers generated by the active LLM.
\newline \newline A chat input field accepts user queries, rendering responses in a multi-turn scrollable chat thread. Each AI response includes an expandable Source Citations panel displaying the exact retrieved text chunks from Pinecone, complete with cosine relevance scores, source type indicators, and source page numbers, providing full transparency on answer grounding. Below as shown in Figure \ref{fig:proto3} is the RAG Q\&A interface.

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.4.png}
  \caption{Prototype 3 — Interactive RAG Question-Answering Interface with Source Citations}
  \label{fig:proto3}
\end{figure}

The key components visible in this interface are: the chat input field for natural language queries; the multi-turn chat conversation thread; the LLM-generated grounded answer; the expandable source citations panel showing chunk text, relevance score, and page number; and the active session model indicator.

\subsection{Prototype 4: Detailed Executive Summary Modal Interface}
The central summary panel includes a dedicated Read Elaborated Summary (300–500 words) action button. Clicking this button opens an interactive modal dialog window (render\_elaborated\_summary\_modal), presenting a comprehensive executive research breakdown.
\newline \newline The modal window features a Spotify-dark header card displaying the paper title, academic field tag, and difficulty badge. The summary text is parsed into four distinct executive breakdown cards: Core Problem \& Research Context (🎯), Proposed Methodology \& Key Innovations (⚙️), Critical Findings \& Benchmarks (📈), and Broader Impact \& Future Directions (🔮). Each section card is styled with a left 4px Spotify Green accent border (\#1DB954) and glowing green section headers (\#1ED760). A stats footer displays total word count, 100\% grounding verification, and the active LLM engine. Below as shown in Figure \ref{fig:proto4} is the Detailed Executive Summary Modal interface.

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.5.png}
  \caption{Prototype 4 — Detailed Executive Summary Modal Interface}
  \label{fig:proto4}
\end{figure}

The key components visible in this interface are: the modal header banner with paper title and metadata tags; the four structured executive breakdown cards with Spotify Green accent borders; the icon-anchored section titles; the scrollable dark summary container; and the executive stats footer displaying word count, grounding status, and active LLM model.

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
paper\_summary & Dict & Cached structured summary including problem, method, findings, keywords, and 300–500 word elaborated summary \\
\hline
full\_text & String & Full extracted normalized plain-text body of the PDF \\
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

\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/4.6.png}
  \caption{Automated Benchmark Scoring Pipeline Architecture}
  \label{fig:evalarch}
\end{figure}

\section{Chapter Summary}
This chapter presented the practical implementation of InsightPaper AI across all system components. The MVC codebase structure was demonstrated through key module implementations including the Groq API model router, Pinecone RAG pipeline, and Streamlit session state manager. Four annotated UI prototype screenshots illustrated the Document Upload and Model Selection interface in Prototype 1, the Main Dashboard with Summary in Prototype 2, the interactive Q\&A Interface in Prototype 3, and the Detailed Executive Summary Modal in Prototype 4. The dataset evaluation pipeline and cross-session state persistence mechanisms were also detailed. Chapter 5 addresses the critical research contribution of this project: the domain-specific fine-tuning of the SentenceTransformer embedding model.

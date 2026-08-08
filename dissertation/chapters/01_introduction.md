\chapter{Introduction}

\section{Background}

% This is a citation \citep{van2019sustainable}. Citations should be made using the \texttt{natbib} package, using the \texttt{citep} and \texttt{citet} commands.

The volume of scientific literature published globally continues to expand at an unprecedented rate. According to recent bibliometric analyses, the number of peer-reviewed articles published annually has grown exponentially over the past two decades, with major indexing services such as PubMed, IEEE Xplore, and arXiv collectively hosting millions of new preprints and journal publications each year (Bornmann and Mutz, 2015). Researchers, postgraduate students, and academic professionals across virtually all technical disciplines now face an overwhelming corpus of papers, conference proceedings, and technical reports that cannot feasibly be read in their entirety during a single literature review cycle. This information overload introduces significant cognitive burden, productivity bottlenecks, and increased risk of overlooking relevant prior work.

  Traditional approaches to literature review manual reading, keyword-based database searches, and citation chaining remain effective for targeted queries but scale poorly as publication volumes increase. Conventional keyword matching algorithms, such as TF-IDF and BM25, rely on literal token overlap between queries and documents, fundamentally limiting their ability to capture semantic synonyms, paraphrases, or conceptual relationships expressed in different vocabulary (Robertson and Zaragoza, 2009). A researcher searching for "methodology employed in the study" would fail to retrieve passages describing "experimental setup" or "algorithmic implementation" unless those exact terms appeared in the text. This lexical gap between how researchers formulate questions and how authors express ideas in papers represents a fundamental limitation of traditional information retrieval.

  The emergence of transformer-based deep learning architectures (Vaswani et al., 2017) and pre-trained Large Language Models (LLMs) has fundamentally transformed the natural language processing landscape. Models such as Meta's LLaMA (Touvron et al., 2023), Alibaba Cloud's Qwen (Yang et al., 2024), and OpenAI's GPT series demonstrate remarkable capabilities in text comprehension, summarisation, and question answering across diverse domains. However, deploying LLMs directly for academic question answering introduces a critical reliability concern: hallucination. When prompted with questions about papers they have not been trained on, LLMs frequently generate plausible-sounding but factually incorrect or entirely fabricated responses (Ji et al., 2023). In academic contexts, where factual precision and source traceability are paramount, hallucinated outputs can mislead researchers and compromise the integrity of literature reviews.

  Retrieval-Augmented Generation (RAG) has emerged as the leading architectural paradigm for addressing LLM hallucination in knowledge-intensive tasks (Lewis et al., 2020). Rather than relying solely on the parametric knowledge stored within a language model's weights, RAG systems first retrieve relevant passages from an external knowledge base and then inject these passages as grounding context into the generation prompt. By constraining the LLM to answer based strictly on retrieved source material, RAG architectures substantially reduce hallucination while enabling source citations that allow users to verify and trace every claim back to the original document. This combination of semantic retrieval accuracy and generative fluency positions RAG as a particularly promising architecture for building research paper analysis tools.

  Recent advances in dense vector representation learning, specifically Sentence-BERT (Reimers and Gurevych, 2019) and lightweight variants such as all-MiniLM-L6-v2, further enhance retrieval quality by projecting text into continuous semantic vector spaces where geometric distance directly measures conceptual similarity. When combined with cloud-native vector databases such as Pinecone, which provide scalable high-dimensional indexing with sub-second query latency, these embedding models enable real-time semantic search across large document collections. Furthermore, contrastive fine-tuning techniques using objectives such as MultipleNegativesRankingLoss (Henderson et al., 2017) allow domain adaptation of general-purpose embedders to specialised corpora such as scientific papers significantly improving retrieval precision for academic question answering.

  It is within this technological context that InsightPaper AI is conceived: a full-stack, end-to-end RAG system designed specifically for grounded research paper analysis, combining fine-tuned semantic retrieval, multi-model LLM generation, and an interactive evaluation framework.

Below as shown in Figure \ref{fig:fig01} is a graph illustrating the growth in annual scientific publications over the past 20-24 years, highlighting the increasing volume of research literature and the resulting information overload.

% Blah as shown in Figure \ref{fig:fig01}. And with \gls{cvd}, which is abbreviated as \gls{cvd}.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/1.1.png}

\caption{Growth of Scientific Publications}

\label{fig:fig01}

\end{figure}

\section{Problem Statement}

Despite the transformative potential of LLMs and semantic search technologies, several critical challenges persist in applying these tools effectively to academic research paper analysis:

\subsection{Hallucination and factual unreliability} General-purpose LLMs, when prompted with questions about specific research papers, frequently generate responses that contain fabricated claims, incorrect numerical results, or misattributed findings. Without access to the actual paper content during generation, the model relies on probabilistic patterns learned during pre-training, which may not accurately reflect the specific paper under analysis. This lack of grounding makes direct LLM querying unsuitable for rigorous academic work where precision and verifiability are essential.

\subsection{Lexical gap in retrieval}

Traditional keyword-based search systems fail to bridge the vocabulary mismatch between how researchers formulate questions and how academic authors express ideas. Dense semantic retrieval using pre-trained sentence transformers offers a solution, but general-purpose embedding models trained on broad web corpora may not adequately capture the specialised vocabulary, structural conventions, and discourse patterns characteristic of scientific literature. Domain-specific fine-tuning is required to close this gap, yet the effectiveness of such fine-tuning for RAG-based academic question answering remains underexplored.

\subsection{Lack of integrated evaluation frameworks}

Existing RAG prototypes and commercial tools for paper analysis rarely provide built-in mechanisms for quantitatively evaluating answer quality. Without automated metrics comparing generated answers to gold-standard references, users cannot objectively assess system reliability. A robust evaluation framework encompassing token-level accuracy, semantic alignment, and holistic quality judgement is needed.

\subsection{Limited multi-model flexibility}

Most existing systems are locked to a single LLM, preventing researchers from comparing response quality, inference latency, and reasoning depth across different model architectures and parameter scales. The ability to switch between models,for example, between a high-capacity reasoning model and a lightweight, low-latency model would provide valuable flexibility for different use cases.

  These challenges collectively motivate the development of InsightPaper AI: a system that integrates fine-tuned dense retrieval, multi-model LLM generation with source grounding, and a comprehensive automated evaluation framework within a single, accessible web application.

\section{Aim and Objectives}

% Blah as shown in Figure \ref{fig:fig01}. And with \gls{cvd}, which is abbreviated as \gls{cvd}.

% \begin{figure}[H]

%   \includegraphics[width=0.9\linewidth]{figures/iris.png}

%   \caption{My figure}

%   \label{fig:fig01}

% \end{figure}

The overarching aim of this project is to design, implement, and evaluate InsightPaper AI, a Retrieval-Augmented Generation system that enables researchers to upload scientific papers as PDFs and receive accurate, source-grounded answers to natural language questions, supported by verifiable source citations and automated quality evaluation. To achieve this aim, the following specific objectives are defined:

\begin{itemize}

\item To develop an end-to-end Retrieval-Augmented Generation (RAG) system for uploading academic papers and generating source-grounded answers with citations.

\item To fine-tune the embedding model to improve retrieval performance on scientific papers and evaluate it using Recall@K and Mean Reciprocal Rank (MRR).

\item To integrate multiple large language models through the Groq API, with user-selectable models and an automatic fallback mechanism.

\item To evaluate the system using token-level F1 score, semantic similarity, and LLM-as-a-Judge metrics for faithfulness, relevance, and completeness.

\item To build a user-friendly Streamlit web application that supports PDF upload, paper summarisation, semantic search, figure extraction, and chat-based question answering.

\end{itemize}

\section{Research Questions}

This project is guided by one primary research question and three supporting sub-questions:

\begin{itemize}

\item Primary Research Question (RQ):

How effectively can a Retrieval-Augmented Generation (RAG) system generate accurate and source-grounded answers from academic research papers?

Sub-Questions

\item Sub Questions 1(SQ1):

Does fine-tuning the embedding model improve retrieval performance compared to the baseline model?

\item Sub Questions 2(SQ2):

How do Qwen 3.6 27B and LLaMA 3.1 8B compare in terms of answer quality and response time?

\item Sub Questions 3(SQ3):

How effective are F1 score, semantic similarity, and LLM-as-a-Judge metrics in evaluating RAG-generated answers?

\end{itemize}

\section{Thesis Structure}

Blah

\begin{itemize}

\item Blah

\item Blah

\end{itemize}

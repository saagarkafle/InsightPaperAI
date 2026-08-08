
\chapter{Embedding Model Fine-Tuning}

\section{Introduction}
The embedding model is the foundational retrieval component of the InsightPaper AI RAG pipeline. It is responsible for mapping both document chunks and user queries into a shared dense vector space, where semantic similarity can be measured via cosine distance. The accuracy of downstream question-answering is directly bounded by retrieval precision: if the correct context chunks are not retrieved, no amount of LLM capability can compensate for missing information.
\newline \newline Initial experimentation using the unmodified sentence-transformers/all-MiniLM-L6-v2 base model on the 30 held-out evaluation papers yielded a Recall@5 of only 23.3\% and a Mean Reciprocal Rank of 0.1161. This demonstrated that the general-domain base embedder was systematically failing to distinguish between semantically similar but topically different academic paper chunks. Domain-specific fine-tuning was therefore identified as a necessary research intervention.
\newline \newline This chapter documents the complete fine-tuning lifecycle: base model selection, dataset preparation, training configuration, and empirical evaluation of the resulting fine-tuned model.

\section{Base Model Selection}

\subsection{Candidate Model Analysis}
Three candidate embedding architectures were evaluated as potential base models before selecting the final pre-training foundation. Table \ref{tab:basemodels} presents the comparative analysis.

\begin{table}[h]
\centering
\caption{Comparative Analysis of Candidate Embedding Model Architectures}
\label{tab:basemodels}
\begin{tabular}{|p{3.5cm}|p{2cm}|p{2cm}|p{2.5cm}|p{3cm}|}
\hline
\textbf{Model} & \textbf{Dim} & \textbf{Parameters} & \textbf{Inference Speed} & \textbf{Memory} \\
\hline
all-MiniLM-L6-v2 & 384 & 22.7M & ~1,400 q/sec & ~90 MB \\
\hline
bge-small-en-v1.5 & 384 & 33.4M & ~900 q/sec & ~130 MB \\
\hline
e5-base-v2 & 768 & 109.5M & ~350 q/sec & ~440 MB \\
\hline
\end{tabular}
\end{table}

\subsection{Selection Rationale}
sentence-transformers/all-MiniLM-L6-v2 was selected as the base model for the following reasons.
\newline \newline Inference Efficiency: At 22.7 million parameters, the model delivers approximately 1,400 queries per second on CPU inference, a critical consideration for a locally deployable application. Larger models such as e5-base-v2 at 109.5 million parameters would significantly increase per-query latency, degrading the interactive user experience.
\newline \newline Embedding Dimensionality: The 384-dimensional output vector strikes a practical balance between representational capacity and Pinecone storage overhead. Larger 768-dimensional models would double storage requirements without guaranteed proportional gains in retrieval accuracy for the target academic domain after fine-tuning.
\newline \newline Fine-Tuning Compatibility: The model's 6-layer architecture supports efficient gradient updates with smaller batch sizes, making domain-adaptive contrastive fine-tuning tractable without requiring multi-GPU hardware.
\newline \newline Pre-Training Coverage: all-MiniLM-L6-v2 was originally trained on over one billion sentence pairs using knowledge distillation from a larger teacher model, providing strong general semantic representations as a fine-tuning starting point.

\section{Dataset Preparation}

\subsection{Dataset Source}
The fine-tuning dataset was sourced from the Kaggle Summarized Research Papers dataset (tyagi586/summarized-research-papers). This dataset contains 150 multi-disciplinary academic research paper records, each providing a title, abstract, summary, and keywords field. The multi-disciplinary nature of the dataset, spanning computer science, biology, physics, and social sciences, was intentional, as InsightPaper AI is designed to handle research papers across all academic domains rather than a single narrow field.

\subsection{Train and Evaluation Split}
The dataset was partitioned into a deterministic 80/20 split using a fixed random seed to ensure reproducibility across training runs. The training set comprised 120 papers used to generate anchor-positive training pairs, and the evaluation set comprised 30 papers held out exclusively for post-training Recall@5 and MRR benchmarking. This split was implemented in scripts/prepare\_kaggle\_dataset.py, which produces two JSONL files: data/kaggle\_train.jsonl and data/kaggle\_eval.jsonl. Table \ref{tab:split} presents the dataset statistics.

\begin{table}[h]
\centering
\caption{Dataset Split and Anchor-Positive Pair Statistics}
\label{tab:split}
\begin{tabular}{|p{3.5cm}|p{2.5cm}|p{4cm}|p{3cm}|}
\hline
\textbf{Split} & \textbf{Papers} & \textbf{Pairs Generated} & \textbf{File} \\
\hline
Training (80\%) & 120 & Approximately 480 anchor-positive pairs & data/kaggle\_train.jsonl \\
\hline
Evaluation (20\%) & 30 & 30 evaluation queries & data/kaggle\_eval.jsonl \\
\hline
\end{tabular}
\end{table}

\subsection{Contrastive Pair Construction}
MultipleNegativesRankingLoss requires training data in the form of anchor-positive text pairs, where the anchor is a short query or sentence and the positive is the semantically corresponding passage from the same document. For each training paper, pairs were constructed by taking a sentence from the paper's summary or abstract field as the anchor, representing a natural language query a researcher might ask, and taking the corresponding passage from the abstract or summary body as the positive, representing the context that directly addresses the anchor.
\newline \newline This strategy simulates realistic query-to-passage alignment, training the embedder to pull together semantically related academic text from the same paper while implicitly separating chunks from different papers. Below as shown in Figure \ref{fig:datapipeline} is the contrastive pair extraction and preprocessing pipeline.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/5.1.png}
  \caption{Contrastive Anchor-Positive Pair Extraction Pipeline}
  \label{fig:datapipeline}
\end{figure}

\section{Training Configuration}

\subsection{Loss Function: MultipleNegativesRankingLoss}
MultipleNegativesRankingLoss (Henderson et al., 2017; Reimers and Gurevych, 2019) is a contrastive learning objective function that leverages in-batch negatives to train dense retrieval models efficiently without requiring manually labelled negative examples.
\newline \newline Given a batch of N anchor-positive pairs, MNRL treats every positive passage belonging to a different anchor within the same batch as a hard negative. For a batch of size 16, each training example effectively receives 15 in-batch negative samples simultaneously. The loss function is defined as follows, where sim denotes the cosine similarity between encoded anchor and positive vectors and the summation runs over all in-batch positives.
\newline \newline In plain terms, this objective pulls each question closer to its correct context in vector space while pushing it away from unrelated contexts in the batch. Below as shown in Figure \ref{fig:mnrl} is a diagram illustrating the in-batch negative contrastive learning mechanics.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/5.2.png}
  \caption{In-Batch Negative Contrastive Learning Mechanics (MultipleNegativesRankingLoss)}
  \label{fig:mnrl}
\end{figure}

\subsection{Hyperparameter Configuration}
Table \ref{tab:hyperparams} presents the complete fine-tuning hyperparameter specifications used for training the InsightPaper-Embed model.

\begin{table}[h]
\centering
\caption{Fine-Tuning Training Hyperparameter Specifications}
\label{tab:hyperparams}
\begin{tabular}{|p{4.5cm}|p{4cm}|p{5cm}|}
\hline
\textbf{Hyperparameter} & \textbf{Value} & \textbf{Justification} \\
\hline
Base Model & all-MiniLM-L6-v2 & Lightweight, fast, strong pre-training foundation \\
\hline
Loss Function & MultipleNegativesRankingLoss & Efficient contrastive learning with in-batch negatives \\
\hline
Training Epochs & 3 & Sufficient convergence without overfitting on 120-paper set \\
\hline
Batch Size & 16 & Provides 15 in-batch negatives per anchor \\
\hline
Optimizer & AdamW & Standard transformer fine-tuning optimizer \\
\hline
Final Training Loss & 0.3387 & Recorded at end of epoch 3 \\
\hline
Output Artifact & models/fine\_tuned\_embedder/ & Saved SentenceTransformer model directory \\
\hline
\end{tabular}
\end{table}

\subsection{Training Execution}
Fine-tuning was executed via scripts/finetune\_embedder.py. The script loads the training pairs from data/kaggle\_train.jsonl, initialises the base all-MiniLM-L6-v2 model, configures the MNRL loss, and runs the training loop for 3 epochs. Upon completion, the fine-tuned model weights are saved to models/fine\_tuned\_embedder/. When InsightPaper AI is subsequently launched, src/rag\_pipeline.py detects the presence of this directory and automatically loads the fine-tuned embedder in preference to the base model.

\section{Model Evaluation: Recall@5 and MRR Benchmark}

\subsection{Evaluation Methodology}
Post-training retrieval performance was evaluated using scripts/eval\_rag.py across all 30 held-out evaluation papers in data/kaggle\_eval.jsonl. For each evaluation paper, a query was constructed from its summary and submitted to the embedding model. The resulting query vector was compared via cosine similarity against all indexed paper chunk vectors, and the rank position of the correct paper's chunks within the returned results was recorded.
\newline \newline Recall@K measures the proportion of queries for which at least one relevant chunk appeared within the top-K results, with K set to 5 as the primary benchmark. Mean Reciprocal Rank computes the average of the reciprocal rank of the first correct result across all queries, where an MRR of 1.0 indicates the correct chunk was ranked first for every query.

\subsection{Benchmark Results}
Table \ref{tab:retrieval} presents the corpus-wide retrieval benchmark results comparing the base model against the fine-tuned model.

\begin{table}[h]
\centering
\caption{Corpus-Wide Retrieval Benchmark Results — Base vs Fine-Tuned Embedder}
\label{tab:retrieval}
\begin{tabular}{|p{4.5cm}|p{2cm}|p{1.5cm}|p{3.5cm}|p{2cm}|}
\hline
\textbf{Model Variant} & \textbf{Recall@5} & \textbf{MRR} & \textbf{Correct in Top-5} & \textbf{Latency} \\
\hline
Base Model (all-MiniLM-L6-v2) & 23.33\% & 0.1161 & 7 / 30 & ~12ms \\
\hline
Fine-Tuned Model & 100.00\% & 1.0000 & 30 / 30 & ~12ms \\
\hline
Absolute Improvement & +76.67pp & +0.8839 & +23 papers & 0ms overhead \\
\hline
\end{tabular}
\end{table}

Below as shown in Figure \ref{fig:recall} is a comparative bar chart illustrating the Recall@5 and MRR performance comparison between the base and fine-tuned models.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/5.3.png}
  \caption{Recall@5 and MRR Performance Comparison — Base vs Fine-Tuned Embedder}
  \label{fig:recall}
\end{figure}

Below as shown in Figure \ref{fig:losscurve} is the training loss curve recorded over the three fine-tuning epochs.

\begin{figure}
  \includegraphics[width=0.9\linewidth]{figures/5.4.png}
  \caption{Training Loss Curve over 3 Fine-Tuning Epochs (Final Loss: 0.3387)}
  \label{fig:losscurve}
\end{figure}

\subsection{Analysis and Discussion}
The dramatic performance gap between the base and fine-tuned models demonstrates that the general-domain semantic space of all-MiniLM-L6-v2 was poorly calibrated for academic retrieval tasks. Research papers from different domains frequently share surface-level scientific vocabulary — terms such as model, training, dataset, and accuracy — that causes high cosine similarity between semantically unrelated paper chunks. The base model was systematically retrieving chunks from wrong papers because these shared terms dominated its vector representations.
\newline \newline Domain-specific contrastive fine-tuning resolved this by training the model to associate complete multi-sentence academic passages from the same paper, pulling together matched anchors and positives while pushing apart passages from different papers. After only 3 epochs of contrastive training on 120 papers, the model's vector space was sufficiently reorganised that every evaluation paper's content was retrievable in rank-1 position.
\newline \newline The fact that MRR reached a perfect 1.0000, not merely Recall@5 of 100\%, confirms that correct chunks were not merely appearing somewhere in the top-5 results but were being ranked first for every query, representing ideal retrieval performance. Crucially, the fine-tuning process introduced no inference latency overhead: both models operate at approximately 12ms per query embedding, confirming that domain adaptation was achieved at zero runtime cost.

\section{Chapter Summary}
This chapter documented the complete embedding model fine-tuning lifecycle for InsightPaper AI. The all-MiniLM-L6-v2 model was selected as the base architecture based on its inference efficiency, fine-tuning tractability, and pre-training quality. A 150-paper Kaggle academic dataset was partitioned into an 80/20 train-evaluation split, and anchor-positive pairs were constructed using abstract and summary sentences to simulate realistic academic retrieval queries. Fine-tuning using MultipleNegativesRankingLoss over 3 epochs with a batch size of 16 achieved a final training loss of 0.3387. Post-training evaluation demonstrated a Recall@5 improvement from 23.33\% to 100\% and MRR improvement from 0.1161 to 1.0000, validating the core research hypothesis of this project. Chapter 6 presents the full results and comparative evaluation of the generative QA components.

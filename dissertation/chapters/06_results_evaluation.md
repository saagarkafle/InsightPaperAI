\chapter{Results and Evaluation}

\section{Introduction}

This chapter presents the empirical evaluation of InsightPaper AI across both its retrieval and generative components. The evaluation is structured around the three sub-questions identified in Chapter 1. The first asks how significantly domain-specific fine-tuning improves retrieval accuracy over the base embedder. The second asks how Qwen 3.6 27B compares to LLaMA 3.1 8B in terms of generated answer quality and inference latency. The third asks whether Token-Level F1, Semantic Similarity, and LLM-as-a-Judge provide complementary evaluation signals and which metric best captures answer quality for academic RAG.

  The evaluation methodology was designed to be fully automated and reproducible using scripts in the scripts/ directory, with all results verifiable by re-running the provided evaluation commands.

\section{Retrieval Evaluation: Base vs Fine-Tuned Embedder}

\subsection{Experimental Setup}

Retrieval evaluation was conducted using scripts/eval\_rag.py on the 30 held-out evaluation papers from data/kaggle\_eval.jsonl. Each paper's abstract or summary sentence served as the evaluation query. Both the base model and the fine-tuned model were evaluated under identical conditions: the same Pinecone index, the same query set, and the same top\_k=5 retrieval parameter.

  Recall@5 measures the fraction of queries for which the correct paper's content appeared in the top-5 retrieved chunks. Mean Reciprocal Rank measures how highly the correct chunk was ranked, computed as the mean of the reciprocal rank of the first correct result across all queries.

\subsection{Results}

Table \ref{tab:retrieval_results} presents the retrieval performance comparison between the base and fine-tuned embedding models.

\begin{table}[H][H]

\centering

\caption{Retrieval Performance — Base vs Fine-Tuned Embedding Model}

\label{tab:retrieval_results}

\begin{tabular}{|p{4.5cm}|p{2cm}|p{1.5cm}|p{3cm}|p{2cm}|}

\hline

\textbf{Model} & \textbf{Recall@5} & \textbf{MRR} & \textbf{Correct in Top-5} & \textbf{Latency} \\

\hline

Base (all-MiniLM-L6-v2) & 23.33\% & 0.1161 & 7 / 30 & ~12ms \\

\hline

Fine-Tuned (InsightPaper-Embed) & 100.00\% & 1.0000 & 30 / 30 & ~12ms \\

\hline

Absolute Improvement & +76.67pp & +0.8839 & +23 papers & 0ms overhead \\

\hline

\end{tabular}

\end{table}

Below as shown in Figure \ref{fig:retrieval_chart} is a comparative bar chart illustrating the Recall@5 and MRR improvement achieved by the fine-tuned model.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/6.1.png}

\caption{Recall@5 and MRR Comparison — Base vs Fine-Tuned Embedder}

\label{fig:retrieval_chart}

\end{figure}

\subsection{Discussion}

The results demonstrate a transformational improvement in retrieval accuracy following domain-specific fine-tuning. The base model correctly retrieved relevant content for only 7 of 30 evaluation papers, a failure rate of 76.7\%. This failure is attributable to the semantic overlap between surface-level scientific vocabulary across unrelated papers. Terms such as classification, accuracy, training set, and baseline model appear frequently in papers from all academic disciplines, causing the general-domain vector space to conflate unrelated passages.

  The fine-tuned model eliminated all retrieval failures. Achieving a perfect MRR of 1.0000, not merely Recall@5 of 100\%, confirms that the correct chunk was ranked first for every single evaluation query, representing an ideal retrieval outcome. This validates the central hypothesis: that domain-adaptive contrastive fine-tuning using MultipleNegativesRankingLoss effectively reorganises the shared embedding space to align with academic retrieval requirements.

  Importantly, this performance improvement was achieved at zero inference latency overhead. Both models operated at approximately 12ms per query embedding, confirming that domain adaptation does not compromise interactive response performance.

\section{Generative QA Evaluation: Qwen 3.6 27B vs LLaMA 3.1 8B}

\subsection{Experimental Setup}

Generative QA evaluation was conducted using scripts/compare\_models.py. This script submitted an identical set of academic questions through the complete RAG pipeline for both models, then evaluated each generated answer using the LLM-as-a-Judge methodology (Zheng et al., 2023). The judge model was prompted to rate each answer on a 1 to 5 integer scale across three dimensions: Faithfulness, which checks whether the answer relies exclusively on the retrieved context; Relevance, which checks whether the answer directly addresses the question; and Completeness, which checks whether the answer covers all key aspects without leaving important elements unaddressed. All evaluation output was captured to output/model\_comparison.txt.

\subsection{Results}

Table \ref{tab:llm_results} presents the LLM comparative evaluation results across both models.

\begin{table}[H][H]

\centering

\caption{LLM Comparative Evaluation Results — Qwen 3.6 27B vs LLaMA 3.1 8B}

\label{tab:llm_results}

\begin{tabular}{|p{3cm}|p{3.5cm}|p{2.5cm}|p{2.5cm}|p{2cm}|}

\hline

\textbf{Model} & \textbf{Groq Model ID} & \textbf{Faithfulness} & \textbf{LLM Judge Score} & \textbf{Avg Latency} \\

\hline

Qwen 3.6 27B & qwen/qwen3.6-27b & 5.00 / 5.0 & 5.00 / 5.0 & 1,996.4 ms \\

\hline

LLaMA 3.1 8B & llama-3.1-8b-instant & 5.00 / 5.0 & 4.47 / 5.0 & 421.3 ms \\

\hline

\end{tabular}

\end{table}

Below as shown in Figure \ref{fig:llm_chart} is a comparison chart illustrating the LLM Judge score and latency trade-off between the two models.

\begin{figure}[H]

\includegraphics[width=0.9\linewidth]{figures/6.2.png}

\caption{LLM-as-a-Judge Overall Score and Latency Comparison — Qwen 3.6 27B vs LLaMA 3.1 8B}

\label{fig:llm_chart}

\end{figure}

\subsection{Discussion}

Both models achieved a perfect Faithfulness score of 5.00 out of 5.00. This result confirms that the strict system prompt, which instructs both models to answer only from provided context and never from their training data, was effective for both architectures at eliminating hallucination entirely. Zero hallucination was observed across all evaluated questions regardless of model scale.

  Qwen 3.6 27B achieved a perfect overall LLM Judge score of 5.00, while LLaMA 3.1 8B scored 4.47. The 0.53-point gap is attributable to LLaMA's more concise response style: while factually accurate and well-grounded, LLaMA's 8-billion parameter capacity produces shorter, sometimes incomplete explanations compared to Qwen's 27-billion parameter multi-paragraph reasoning. The LLM-as-a-Judge penalty for LLaMA was primarily attributed to the Completeness dimension.

  LLaMA 3.1 8B delivered a 421.3ms average response latency, approximately 4.7 times faster than Qwen 3.6 27B at 1,996.4ms. This latency advantage makes LLaMA the preferred option for users who prioritise interactive responsiveness over exhaustive analytical depth.

  The dual-model architecture of InsightPaper AI is therefore empirically justified: Qwen 3.6 27B is optimal for detailed research analysis tasks, while LLaMA 3.1 8B is optimal for rapid iterative querying.

\section{Evaluation Metric Analysis}

\subsection{Complementarity of the Three-Metric Framework}

The three evaluation metrics used in InsightPaper AI capture qualitatively different aspects of answer quality. Table \ref{tab:metric_comparison} presents the complementarity analysis.

\begin{table}[H][H]

\centering

\caption{Evaluation Metric Complementarity Analysis}

\label{tab:metric_comparison}

\begin{tabular}{|p{3cm}|p{4cm}|p{4cm}|p{3cm}|}

\hline

\textbf{Metric} & \textbf{Strength} & \textbf{Limitation} & \textbf{Best Captures} \\

\hline

Token-Level F1 & Objective and reproducible; no model dependency & Penalises correct paraphrases; vocabulary-sensitive & Exact phrasing overlap \\

\hline

Semantic Similarity & Vocabulary-agnostic; captures meaning alignment & Cannot detect hallucinated but fluent text & Conceptual alignment between generated and reference \\

\hline

LLM-as-a-Judge & Captures completeness, depth, and qualitative faithfulness & Requires additional LLM inference; judge bias possible & Holistic answer quality including reasoning depth \\

\hline

\end{tabular}

\end{table}

In isolation, each metric is insufficient. Token F1 penalises answers that correctly paraphrase using different words. Semantic Similarity cannot distinguish a factually incorrect but stylistically similar answer from a correct one. LLM-as-a-Judge is subjective and introduces additional LLM-induced variance. Together, the three metrics provide a triangulated, robust signal: a high-quality answer should score well on all three simultaneously.

\subsection{System Latency Profile}

Table \ref{tab:latency} presents the end-to-end query latency breakdown for both model configurations.

\begin{table}[H][H]

\centering

\caption{End-to-End Query Latency Breakdown}

\label{tab:latency}

\begin{tabular}{|p{4cm}|p{4cm}|p{4cm}|}

\hline

\textbf{Stage} & \textbf{Component} & \textbf{Avg Latency} \\

\hline

Query Embedding & Fine-Tuned SentenceTransformer on CPU & ~12ms \\

\hline

Vector Retrieval & Pinecone Top-5 Cosine Search & ~40ms \\

\hline

LLM Generation (Qwen 3.6 27B) & Groq LPU Inference & ~1,944ms \\

\hline

LLM Generation (LLaMA 3.1 8B) & Groq LPU Inference & ~369ms \\

\hline

Total (Qwen 3.6 27B) & — & ~1,996ms \\

\hline

Total (LLaMA 3.1 8B) & — & ~421ms \\

\hline

\end{tabular}

\end{table}

The embedding and retrieval stages are negligible relative to LLM generation time, confirming that the fine-tuned embedding model introduces no meaningful latency overhead into the user-facing response cycle. The dominant latency contributor is always the generative model inference step.

\section{Limitations}

Several limitations of the current evaluation are acknowledged.

  The evaluation dataset size of 30 held-out papers provides a useful benchmark but a larger evaluation corpus would provide stronger statistical confidence in the Recall@5 and MRR results. A set of several hundred papers across more diverse disciplines would be more representative of production use.

  There is also a potential LLM-as-a-Judge bias concern. The judge model used for evaluation in some configurations is the same Qwen 3.6 27B used as the primary generative model. This introduces potential self-preference bias, where the judge may implicitly favour answers stylistically similar to its own generation patterns.

  Additionally, fine-tuning was performed on 120 training papers, which is a relatively small corpus by deep-learning standards. Fine-tuning on a larger multi-domain academic corpus such as ArXiv full papers may yield further retrieval improvements and better generalisation to highly specialised domains.

  Finally, all evaluation was conducted automatically. Human expert assessment of answer quality for a subset of questions would provide additional external validation of the LLM-as-a-Judge scores and establish the degree to which automated evaluation aligns with expert human judgement.

\section{Chapter Summary}

This chapter presented empirical evaluation across both components of InsightPaper AI. Retrieval evaluation demonstrated that domain-specific fine-tuning using MNRL transformed Recall@5 from 23.33\% to 100\% and MRR from 0.1161 to 1.0000 at zero inference latency overhead. Generative QA evaluation showed that both Qwen 3.6 27B and LLaMA 3.1 8B achieved perfect Faithfulness of 5.00 out of 5.00, with Qwen achieving a superior overall LLM Judge score of 5.00 compared to 4.47 at the cost of 4.7 times higher latency. The three-metric evaluation framework was demonstrated to provide complementary signals that together capture a comprehensive picture of RAG system performance. Limitations including small evaluation corpus size and potential judge bias were acknowledged. Chapter 7 synthesises these findings into a conclusion and outlines directions for future work.

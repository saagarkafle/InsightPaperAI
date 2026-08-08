\chapter{Conclusion and Future Work}

\section{Summary of the Project}

This project designed, implemented, and evaluated InsightPaper AI — a web-based Retrieval-Augmented Generation system enabling researchers, students, and academics to upload scientific research papers as PDF documents and interact with their content through natural language questions. The system produces answers grounded exclusively in retrieved paper content, enforcing zero-hallucination through strict prompt engineering, while supporting two state-of-the-art large language models: Meta's LLaMA 3.1 8B and Alibaba Cloud's Qwen 3.6 27B, served via the Groq high-performance inference API.

  The project addressed the primary research question: how effectively can an end-to-end RAG architecture utilising a fine-tuned Sentence-Transformer embedder, Pinecone vector index, and multi-model LLMs retrieve relevant paper contexts and generate accurate, source-grounded answers for academic research papers? The results provide a clear and quantitative answer: extremely effectively, when domain-specific fine-tuning is applied to the retrieval layer.

\section{Summary of Contributions}

\subsection{Contribution 1: Fine-Tuned Academic Retrieval Embedder}

The most significant technical contribution of this project is the domain-specific fine-tuning of the sentence-transformers/all-MiniLM-L6-v2 embedding model using MultipleNegativesRankingLoss contrastive learning on the 150-paper Kaggle Summarized Research Papers dataset. This fine-tuning intervention produced a dramatic retrieval improvement, taking Recall@5 from 23.33\% to 100.00\%, an absolute increase of 76.67 percentage points, and MRR from 0.1161 to 1.0000, an absolute increase of 0.8839. The fine-tuned model achieved perfect retrieval accuracy across all 30 held-out evaluation papers with no increase in inference latency at approximately 12ms per query.

\subsection{Contribution 2: End-to-End RAG System Implementation}

InsightPaper AI is a fully functional, locally deployable RAG web application built using Python, Streamlit, PyMuPDF, SentenceTransformers, Pinecone, and the Groq API. The system implements a complete document processing pipeline from PDF upload through text extraction, overlapping chunk generation, vector indexing, semantic retrieval, and LLM-grounded answer generation. The MVC architectural pattern ensures clean separation of concerns across view, controller, and model layers, producing a maintainable and extensible codebase.

\subsection{Contribution 3: Empirical Multi-Model Comparative Evaluation}

An automated empirical benchmark in scripts/compare\_models.py was developed and executed to quantitatively compare Qwen 3.6 27B and LLaMA 3.1 8B across three evaluation dimensions. Both models achieved perfect Faithfulness of 5.00 out of 5.00, confirming the effectiveness of the strict system prompt grounding strategy. Qwen 3.6 27B achieved superior overall quality with a score of 5.00 compared to 4.47 for LLaMA 3.1 8B, while LLaMA delivered 4.7 times lower latency at 421ms compared to 1,996ms. This empirical comparison provides actionable guidance: Qwen for analytical depth, LLaMA for interactive speed.

\subsection{Contribution 4: Three-Dimensional Evaluation Framework}

The project implemented and applied a three-metric evaluation framework combining Token-Level F1, Semantic Vector Similarity, and LLM-as-a-Judge ratings (Zheng et al., 2023). This framework demonstrated that each metric captures qualitatively distinct aspects of answer quality, and that no single metric is sufficient for comprehensive RAG evaluation. The framework is generalisable to other RAG systems beyond InsightPaper AI.

\section{Research Questions Answered}

\subsection{Primary Research Question}

The primary research question asked how effectively an end-to-end RAG architecture can retrieve relevant paper contexts and generate accurate, source-grounded answers. The answer is extremely effectively. Domain-specific contrastive fine-tuning using MNRL on 120 training papers transformed retrieval from a Recall@5 of 23.33\% to a perfect 100\%, eliminating all 23 retrieval failures observed with the base model. Both generative models produced zero hallucinations when grounded via the RAG system prompt.

\subsection{Sub-Question 1}

The first sub-question asked whether fine-tuning the embedding model improves retrieval performance compared to the baseline. The answer is definitively yes. The fine-tuned model achieved Recall@5 of 100\% and MRR of 1.0000, compared to 23.33\% and 0.1161 for the base model, without any increase in query latency.

\subsection{Sub-Question 2}

The second sub-question asked how Qwen 3.6 27B and LLaMA 3.1 8B compare in terms of answer quality and response time. Both models produce completely faithful, hallucination-free answers when grounded via the RAG system prompt. Qwen 3.6 27B produces more complete and analytically deep responses scoring 5.00 out of 5.0 overall compared to 4.47 for LLaMA 3.1 8B, while LLaMA responds 4.7 times faster. The choice is a quality-latency trade-off, not a quality-accuracy trade-off.

\subsection{Sub-Question 3}

The third sub-question asked how effectively F1 score, semantic similarity, and LLM-as-a-Judge metrics evaluate RAG-generated answers. Each metric captures a qualitatively distinct aspect: Token F1 measures exact vocabulary overlap, Semantic Similarity captures meaning alignment independent of vocabulary, and LLM-as-a-Judge evaluates holistic completeness and explanation depth. The three metrics address each other's blind spots and together provide a robust, triangulated evaluation signal.

\section{Limitations}

Several limitations of the current system and evaluation are acknowledged.

  The retrieval benchmark used only 30 held-out papers. A larger corpus would provide stronger statistical confidence in Recall@5 and MRR results and better test generalisation to highly specialised academic domains not represented in the Kaggle dataset.

  The embedder was fine-tuned solely on the 150-paper Kaggle dataset. Training on a larger, more diverse corpus such as ArXiv abstracts or Semantic Scholar records may improve generalisation further.

  The LLM-as-a-Judge evaluations were conducted using Qwen 3.6 27B as both the primary generative model and the judge model in some test configurations. This introduces potential self-preference bias that human evaluator validation would mitigate.

  The current implementation processes and retrieves from a single active paper per session. Supporting multi-document cross-paper retrieval is currently out of scope.

  The PyMuPDF parser handles standard academic PDFs well but may produce incomplete text extraction on scanned or image-only PDFs, complex multi-column layouts, or papers with non-standard encoding. OCR integration would be required to address these edge cases.

  All evaluation was conducted automatically. Human expert assessment of answer quality for a subset of questions would provide additional validation of the automated metric scores.

\section{Future Work}

\subsection{Multi-Document Cross-Paper Retrieval}

The most impactful near-term extension would be enabling simultaneous retrieval across multiple uploaded papers. A researcher could build a personal library of papers, submit a single query, and receive an answer that synthesises evidence from across the entire corpus with source attribution per paper. This would require namespace management across multiple Pinecone namespaces and a modified prompt template acknowledging multiple source documents.

\subsection{Larger-Scale Embedding Fine-Tuning}

Fine-tuning on a substantially larger academic corpus, such as tens of thousands of ArXiv paper abstracts spanning all major scientific disciplines, would validate the model's generalisation to highly specialised subfields not represented in the 150-paper Kaggle dataset and likely push retrieval performance even further.

\subsection{Figure-Aware Question Answering}

InsightPaper AI extracts figures from PDFs but does not currently incorporate them into the RAG answer pipeline. A multimodal extension using a vision-language model would enable queries referencing specific figures, significantly expanding the system's utility for papers where key findings are communicated visually rather than textually.

\subsection{Human Evaluation Study}

Conducting a controlled human evaluation study with a sample of academic researchers — asking them to rate generated answers using a structured rubric — would provide external validation of the LLM-as-a-Judge scores and establish the degree to which automated evaluation aligns with expert human judgement.

\subsection{Hybrid Retrieval}

Replacing the current dense-only retrieval with a hybrid BM25 and dense vector approach using reciprocal rank fusion could improve retrieval robustness for keyword-specific queries where exact term matching outperforms semantic similarity. Pinecone's integrated sparse-dense hybrid search would enable this without major architectural changes.

\section{Reflection}

This project demonstrated that the bottleneck in academic RAG systems is not the generative model but the retrieval layer. A general-purpose embedding model retrieving wrong context chunks will produce wrong answers regardless of how capable the downstream LLM is. The most impactful single intervention was not model selection or prompt engineering but domain-adaptive fine-tuning of the embedder, which increased retrieval accuracy from 23.33\% to 100\%. This finding reinforces an important principle in RAG system design: the embedder is the foundation, and its domain alignment is non-negotiable for high-stakes retrieval tasks such as academic question answering.

\section{Chapter Summary}

This concluding chapter synthesised the contributions of InsightPaper AI across four dimensions: a fine-tuned academic retrieval embedder achieving Recall@5 of 23.33\% increasing to 100\%, a fully functional end-to-end RAG web application, an empirical multi-model generative evaluation comparing Qwen against LLaMA, and a three-metric evaluation framework. The three research questions were answered quantitatively. Limitations of the current system including evaluation corpus size, single-document scope, and judge bias were honestly acknowledged. Five concrete future directions were outlined, with multi-document cross-paper retrieval and multimodal figure-aware QA identified as the highest-priority extensions. The project conclusively demonstrates that domain-specific contrastive fine-tuning is the critical enabler of reliable academic RAG retrieval performance.

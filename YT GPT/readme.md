# YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that converts YouTube videos into an interactive question-answering system.

This project extracts transcripts from YouTube videos, processes them into semantic chunks, stores embeddings in a vector database, retrieves the most relevant context for a user query, and generates grounded answers using an LLM.

The goal is not just to "chat with a video", but to demonstrate how a modern RAG pipeline works end-to-end.

---

# What This Project Actually Solves

Large Language Models are powerful, but they have a major limitation:

- They do not automatically know the contents of a specific YouTube video.
- They hallucinate when context is missing.
- They cannot reliably answer questions about private or custom data unless that data is injected into the prompt.

This project solves that problem using a RAG architecture.

Instead of training a model from scratch:

1. The transcript is extracted from a YouTube video.
2. The transcript is transformed into embeddings.
3. Those embeddings are stored in a vector database.
4. User questions are converted into embeddings.
5. Similar transcript chunks are retrieved.
6. The retrieved context is injected into the LLM prompt.
7. The LLM generates a grounded answer.

This creates a system that is:

- Faster than fine-tuning
- Cheaper than retraining models
- More reliable for custom knowledge
- Easy to scale to multiple documents/videos

---

# RAG Architecture Overview

## Full Pipeline

```text
YouTube Video
      ↓
Transcript Extraction
      ↓
Text Cleaning
      ↓
Chunking / Splitting
      ↓
Embedding Generation
      ↓
FAISS Vector Store
      ↓
Retriever
      ↓
Prompt Augmentation
      ↓
LLM (Groq + Llama)
      ↓
Final Answer
```

---

# Core Concepts Used

## 1. Data Ingestion

The pipeline begins by fetching transcripts directly from YouTube using:

- `youtube-transcript-api`

The transcript becomes the raw knowledge base.

Example:

```python
transcript_list = YouTubeTranscriptApi().fetch(video_id)
transcript = " ".join(chunk.text for chunk in transcript_list)
```

### Why This Step Matters

Without ingestion, the LLM has no domain-specific context.

This step converts unstructured video content into machine-processable text.

---

## 2. Text Chunking

LLMs and embedding models work poorly with massive blocks of text.

The transcript is divided into overlapping chunks using:

- `RecursiveCharacterTextSplitter`

Example:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)
```

### Why Chunking Is Critical

Bad chunking destroys retrieval quality.

If chunks are:

- Too large → retrieval becomes noisy
- Too small → context gets fragmented

The overlap preserves semantic continuity between chunks.

This is one of the most underestimated parts of RAG systems.

---

## 3. Embedding Generation

Each chunk is converted into a dense vector representation.

The project uses:

- Google Gemini Embeddings

Example:

```python
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2"
)
```

### What Embeddings Actually Do

Embeddings transform text into numerical vectors that capture semantic meaning.

This allows the system to retrieve:

- Similar meaning
- Related concepts
- Contextual relevance

instead of simple keyword matching.

Example:

A query about:

```text
"How does agentic AI differ from generative AI?"
```

can still retrieve chunks containing:

```text
"autonomous systems"
```

because embeddings understand semantic similarity.

---

## 4. Vector Store (FAISS)

The generated embeddings are stored in:

- FAISS (Facebook AI Similarity Search)

Example:

```python
vector_store = FAISS.from_documents(chunks, embeddings)
```

### Why Vector Databases Matter

Traditional databases search exact matches.

Vector databases search by similarity in high-dimensional space.

This is the backbone of modern RAG systems.

FAISS enables:

- Fast nearest-neighbor search
- Semantic retrieval
- Scalable similarity matching

---

## 5. Retrieval Pipeline

The retriever searches the vector store for the most relevant chunks.

Example:

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
```

### Retrieval Flow

```text
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Top-k Relevant Chunks
```

### Why Retrieval Is the Heart of RAG

Most people obsess over the LLM.

The real performance bottleneck in RAG systems is retrieval quality.

Weak retrieval causes:

- Hallucinations
- Irrelevant answers
- Missing context
- Confidently wrong outputs

A strong retriever can dramatically improve even smaller LLMs.

---

## 6. Prompt Augmentation

Retrieved chunks are injected into the final prompt.

Example:

```python
context_text = "\n\n".join(
    doc.page_content for doc in retrieved_docs
)
```

The prompt forces the LLM to answer only from retrieved context.

Example prompt behavior:

```text
Answer ONLY from the provided transcript context.
If the context is insufficient, say you don't know.
```

### Why This Matters

This step grounds the model.

Without grounding:

- The model improvises
- Hallucinations increase
- Trust decreases

With grounding:

- Answers become source-aware
- Responses become more factual
- The system becomes production-usable

---

## 7. Generation Layer

The final answer is generated using:

- Groq inference
- Llama 3.3 70B

Example:

```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
```

### Why Groq?

Groq provides extremely fast inference.

This reduces latency and creates a near real-time chatbot experience.

---

# End-to-End Pipeline Explanation

## Step-by-Step Execution Flow

### Step 1 — Extract Transcript

The system downloads the YouTube transcript.

Output:

```text
Raw unstructured text
```

---

### Step 2 — Split Transcript

The transcript is divided into semantic chunks.

Output:

```text
List of smaller contextual documents
```

---

### Step 3 — Generate Embeddings

Every chunk becomes a numerical vector.

Output:

```text
Vector representations of transcript chunks
```

---

### Step 4 — Store in FAISS

Vectors are indexed for similarity search.

Output:

```text
Searchable vector database
```

---

### Step 5 — User Asks Question

Example:

```text
What is the difference between agentic AI and generative AI?
```

---

### Step 6 — Retrieve Relevant Chunks

Retriever searches semantically similar transcript sections.

Output:

```text
Top-k relevant transcript chunks
```

---

### Step 7 — Augment Prompt

Retrieved chunks are inserted into the LLM prompt.

Output:

```text
Context-aware prompt
```

---

### Step 8 — Generate Answer

The LLM produces a grounded response.

Output:

```text
Final AI-generated answer
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Transcript Extraction | youtube-transcript-api |
| Framework | LangChain |
| Embeddings | Google Gemini Embeddings |
| Vector Database | FAISS |
| LLM Inference | Groq |
| Model | Llama 3.3 70B |
| Notebook Environment | Jupyter Notebook |

---

# Libraries Used

```bash
pip install -q \
youtube-transcript-api \
langchain-community \
langchain-google-genai \
faiss-cpu \
tiktoken \
python-dotenv \
langchain-groq
```

---

# Project Structure

```text
youtube_chatbot.ipynb
│
├── Data Ingestion
├── Transcript Processing
├── Text Chunking
├── Embedding Generation
├── FAISS Vector Store
├── Retriever Setup
├── Prompt Engineering
└── Response Generation
```

---

# Example Workflow

## Input

```text
YouTube Video URL
```

## User Query

```text
What is generative AI?
```

## Internal Pipeline

```text
Query → Embedding → Retrieval → Context Injection → LLM
```

## Output

```text
Grounded answer generated from the transcript
```

---

# Why This Project Is Important

This project demonstrates several real-world AI engineering concepts:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Embeddings
- Vector Databases
- Context Injection
- Prompt Grounding
- LLM Orchestration
- AI Pipelines

---


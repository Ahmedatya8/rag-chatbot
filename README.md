# UAE Real Estate RAG Chatbot

> AI-powered chatbot that answers questions about the Dubai property market
> using official RERA reports and real estate market documents.
> Built with LangChain, ChromaDB, and GPT-3.5-turbo. Deployed on Streamlit.

🔗 **Live Demo:** https://rag-chatbot-ufzgfxcbqqubxbqmyfznfn.streamlit.app/

---

## Problem

Dubai's property market is complex — RERA regulations, area-specific
pricing, transaction trends, and investment insights are spread across
dozens of reports. This chatbot makes that knowledge instantly accessible
through natural language, grounded strictly in official documents.

---

## How It Works
User Question
↓
Embed question with text-embedding-3-small
↓
ChromaDB finds top 4 relevant chunks (MMR)
↓
Chunks + question sent to GPT-3.5-turbo
↓
Grounded answer with source citations

---

## Knowledge Base

| Document | Source |
|---|---|
| RERA Annual Report | Dubai Land Department |
| Dubai Market Report | Knight Frank |
| Real Estate Statistics | Dubai Statistics Center |

---

## Evaluation

| Metric | Result |
|---|---|
| Questions tested | 10 |
| Answered from documents | 9/10 |
| Hallucination-free | 10/10 |
| Sources cited correctly | 9/10 |
| Grounding rate | 100% |

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | GPT-3.5-turbo (OpenAI) |
| Embeddings | text-embedding-3-small (OpenAI) |
| Vector store | ChromaDB |
| RAG framework | LangChain |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## Project Structure
rag-chatbot/
├── data/
│   └── pdfs/                    ← UAE real estate documents
├── notebooks/
│   ├── 01_ingest.ipynb          ← PDF loading, chunking, embedding
│   └── 02_rag_chain.ipynb       ← RAG chain testing and evaluation
├── src/
│   └── retriever.py             ← RAG chain logic
├── app/
│   └── main.py                  ← Streamlit UI
├── vectorstore/                 ← ChromaDB persisted vectors
└── requirements.txt

---

## Run Locally

```bash
# Clone
git clone https://github.com/ahmedatya8/rag-chatbot
cd rag-chatbot

# Install
pip install -r requirements.txt

# Add your OpenAI key
echo 'OPENAI_API_KEY=your-key' > .env

# Run
streamlit run app/main.py
```

---

## RAG Pipeline Design Decisions

| Decision | Rationale |
|---|---|
| Chunk size 1000 chars | Fits in GPT-3.5 context with room for answer |
| Chunk overlap 200 chars | Prevents losing info at chunk boundaries |
| MMR retrieval | Returns diverse chunks — avoids 4 chunks saying the same thing |
| temperature=0 | Deterministic answers — no hallucination from randomness |
| Strict prompt | "ONLY use context" prevents model using training data |
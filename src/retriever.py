# ── Write production retriever module ─────────────────────────────────────────
# Streamlit app imports ask() from here — same pattern as Project 1

retriever_code = '''import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

ROOT       = Path(__file__).resolve().parent.parent
VECTOR_DIR = ROOT / "vectorstore"
API_KEY    = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """You are an expert UAE real estate analyst assistant.
Answer the question using ONLY the context provided below.
If the answer is not found in the context, say exactly:
"I dont have enough information in the provided documents to answer this."

Always cite which document and page number your answer comes from.

Context:
{context}

Question: {question}

Answer (with source citation):"""

# ── Lazy loading — build once, reuse forever ──────────────────────────────────
_chain = None


def get_chain():
    global _chain
    if _chain is None:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=API_KEY
        )
        vectorstore = Chroma(
            persist_directory=str(VECTOR_DIR),
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 10}
        )
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=API_KEY
        )
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        _chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    return _chain


def ask(question: str) -> dict:
    chain  = get_chain()
    result = chain.invoke({"query": question})
    seen, sources = set(), []
    for doc in result["source_documents"]:
        source = doc.metadata.get("source", "unknown")
        page   = doc.metadata.get("page", "?")
        key    = f"{source}::{page}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "filename": Path(source).name,
                "page":     page,
            })
    return {"answer": result["result"], "sources": sources}
'''

src_path = ROOT / 'src' / 'retriever.py'
with open(src_path, 'w') as f:
    f.write(retriever_code)

print(f"src/retriever.py written ✅")
# ── main.py ───────────────────────────────────────────────────────────────────
# Streamlit UI for the UAE Real Estate RAG Chatbot.
# Imports ask() from src/retriever.py — no model logic lives here.

import sys
from pathlib import Path

# ── Make src/ importable ──────────────────────────────────────────────────────
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.retriever import ask

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UAE Real Estate Chatbot",
    page_icon="🏙️",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏙️ UAE Real Estate Chatbot")
st.markdown(
    "Ask anything about the Dubai property market. "
    "Answers are grounded in official RERA and market reports."
)
st.divider()

# ── Chat history ──────────────────────────────────────────────────────────────
# Streamlit reruns the whole script on every interaction.
# st.session_state persists data across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render existing chat history ──────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show sources for assistant messages if they exist
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📄 Sources"):
                for s in message["sources"]:
                    st.markdown(f"- **{s['filename']}** — page {s['page']}")

# ── Chat input ────────────────────────────────────────────────────────────────
if question := st.chat_input("Ask about Dubai real estate..."):

    # ── Display user message ──────────────────────────────────────────────────
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "sources": []
    })
    with st.chat_message("user"):
        st.markdown(question)

    # ── Generate answer ───────────────────────────────────────────────────────
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
                result  = ask(question)
                answer  = result["answer"]
                sources = result["sources"]
            except Exception as e:
                answer  = f"❌ Error: {str(e)}"
                sources = []

        # ── Display answer ────────────────────────────────────────────────────
        st.markdown(answer)

        # ── Display sources in collapsible expander ───────────────────────────
        if sources:
            with st.expander("📄 Sources"):
                for s in sources:
                    st.markdown(f"- **{s['filename']}** — page {s['page']}")

    # ── Save assistant message to history ─────────────────────────────────────
    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": sources
    })

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About")
    st.markdown(
        "This chatbot answers questions using real UAE property "
        "market documents including RERA reports and market analyses."
    )
    st.divider()

    st.header("Sample Questions")
    sample_questions = [
        "What is the current state of Dubai real estate?",
        "Which areas have the highest property prices?",
        "What are RERA regulations for buyers?",
        "What is the outlook for Dubai property in 2024?",
        "How many transactions were recorded last year?",
    ]
    for q in sample_questions:
        st.markdown(f"- {q}")

    st.divider()

    # ── Clear chat button ─────────────────────────────────────────────────────
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built with LangChain · ChromaDB · GPT-3.5-turbo · Streamlit")
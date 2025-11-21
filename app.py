import streamlit as st
from config import config
from models.llm import LLMClient
from utils.rag import (
    add_documents_to_store,
    retrieve_relevant_chunks,
    init_vector_store_in_session,
)
from utils.web_search import web_search_with_duckduckgo

st.set_page_config(page_title="Medical Assistant", page_icon="💊", layout="wide")

# --- Sidebar configuration ---
st.sidebar.title("⚙️ Settings")

response_mode = st.sidebar.radio(
    "Response mode",
    options=["Concise", "Detailed"],
    index=0,
    help="Concise: short answers. Detailed: in-depth explanations.",
)

use_rag = st.sidebar.toggle(
    "Use local medical knowledge (RAG)",
    value=True,
    help="If enabled, the chatbot will ground its answers in the uploaded documents (PDFs).",
)

use_web = st.sidebar.toggle(
    "Use web search (DuckDuckGo)",
    value=True,
    help="If enabled, the chatbot will add brief medical snippets from the web.",
)

temperature = st.sidebar.slider(
    "Creativity (temperature)",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05,
)

st.sidebar.markdown("---")
st.sidebar.subheader("📄 Upload medical reference PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files (patient guides, FAQs, discharge summaries, etc.)",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload trusted medical PDFs. The text will be extracted locally and used for RAG.",
)

# --- Init state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

init_vector_store_in_session()

if uploaded_files:
    for f in uploaded_files:
        try:
            add_documents_to_store(f)
        except Exception as e:
            st.sidebar.error(f"Failed to process {f.name}: {e}")

# --- Header ---
st.title("💊 Medical Information Chatbot (Groq + PDF RAG)")
st.caption(
    "Educational medical assistant with PDF-based RAG + DuckDuckGo web search • "
    "Backed by Groq (llama-3.1-8b-instant) • Not a medical substitute."
)

st.info(
    "⚠️ Disclaimer: This chatbot provides general educational medical information only. "
    "It cannot diagnose conditions, prescribe treatment, or replace a licensed doctor.",
    
)

# --- Chat interface ---
llm_client = LLMClient(temperature=temperature)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a medical question (e.g., 'What are common symptoms of anemia?')")

def build_system_prompt(mode: str) -> str:
    base = (
        "You are a cautious, helpful medical information assistant. "
        "You explain medical topics in simple language for education only.\n\n"
        "SAFETY RULES:\n"
        "- You are not a doctor and cannot diagnose, treat, or prescribe medicines.\n"
        "- Do not give drug names, dosages, or treatment plans.\n"
        "- Do not suggest dangerous actions or home treatments for emergencies.\n"
        "- Encourage users to consult licensed medical professionals for personal advice.\n"
        "- If symptoms sound like an emergency, tell the user to seek emergency care immediately.\n"
    )
    if mode == "Concise":
        base += (
            "\nRESPONSE STYLE:\n"
            "- Keep answers short (2–4 sentences).\n"
            "- Use simple language.\n"
            "- Highlight only key points.\n"
        )
    else:
        base += (
            "\nRESPONSE STYLE:\n"
            "- Provide a structured, detailed explanation with headings and bullet points.\n"
            "- Break down concepts step by step in simple language.\n"
            "- Include typical causes, risk factors, and when to see a doctor.\n"
        )
    return base

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            system_prompt = build_system_prompt(response_mode)

            # --- RAG Context ---
            rag_context = ""
            if use_rag and st.session_state.vector_store["embeddings"] is not None:
                try:
                    top_chunks = retrieve_relevant_chunks(user_input, top_k=5)
                    if top_chunks:
                        rag_context = (
                            "LOCAL MEDICAL NOTES (from uploaded PDFs):\n"
                            + "\n".join(f"- {c}" for c in top_chunks)
                        )
                except Exception as e:
                    st.warning(f"RAG retrieval failed: {e}")

            # --- Web Search Context (DuckDuckGo only) ---
            web_context = ""
            if use_web:
                try:
                    search_results = web_search_with_duckduckgo(user_input, max_results=3)
                    if search_results:
                        web_context = (
                            "WEB SEARCH CONTEXT (DuckDuckGo medical snippets):\n"
                            + search_results
                        )
                except Exception as e:
                    st.warning(f"Web search failed: {e}")

            # Build final system prompt
            full_system_prompt = system_prompt
            if rag_context:
                full_system_prompt += "\n\n" + rag_context
            if web_context:
                full_system_prompt += "\n\n" + web_context

            try:
                assistant_reply = llm_client.chat(
                    system_prompt=full_system_prompt,
                    messages=st.session_state.messages,
                )
            except Exception as e:
                assistant_reply = (
                    "Groq API error: "
                    f"{e}. Check your GROQ_API_KEY in config/config.py."
                )

            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
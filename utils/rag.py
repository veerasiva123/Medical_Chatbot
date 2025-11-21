from typing import List
import numpy as np
import streamlit as st
from pypdf import PdfReader

from models.embeddings import embed_texts


def init_vector_store_in_session():
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = {
            "texts": [],
            "embeddings": None,
        }


def _extract_text_from_pdf(file) -> str:
    """Extract text from an uploaded PDF file object using pypdf."""
    reader = PdfReader(file)
    parts: List[str] = []
    for page in reader.pages:
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt:
            parts.append(txt)
    return "\n".join(parts)


def _chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    text = text.replace("\n", " ").strip()
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def add_documents_to_store(pdf_file):
    """Extract text from a PDF, chunk it, embed with TF-IDF, and store in session."""
    if "vector_store" not in st.session_state:
        init_vector_store_in_session()

    raw_text = _extract_text_from_pdf(pdf_file)
    if not raw_text.strip():
        return

    chunks = _chunk_text(raw_text)
    if not chunks:
        return

    texts = st.session_state.vector_store["texts"] + chunks

    
    vectors = embed_texts(texts, fit=True)

    st.session_state.vector_store["texts"] = texts
    st.session_state.vector_store["embeddings"] = vectors


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    return a_norm @ b_norm.T


def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[str]:
    store = st.session_state.get("vector_store")
    if not store or store["embeddings"] is None or not store["texts"]:
        return []

    query_vec = embed_texts([query], fit=False)[0:1]
    doc_vecs = store["embeddings"]

    sims = _cosine_similarity(query_vec, doc_vecs)[0]
    top_idx = np.argsort(sims)[::-1][:top_k]

    return [store["texts"][i] for i in top_idx]
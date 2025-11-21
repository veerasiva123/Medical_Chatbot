# Medical Information Chatbot – Groq + PDF RAG

- LLM: Groq `llama-3.1-8b-instant` via OpenAI-compatible API
- RAG: Local TF-IDF over text extracted from uploaded PDFs (no embedding API)
- Web search: DuckDuckGo only (free, no key)

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

Edit `config/config.py` and put your Groq key:

```python
GROQ_API_KEY = "gsk_your_real_key_here"
```

Then run:

```bash
streamlit run app.py
```
🩺 Medical Information Chatbot (Groq + PDF RAG)

An educational medical assistant that uses PDF-based RAG, Groq (Llama-3.1-8B-Instant), and DuckDuckGo web search to provide clear, safe, and easy-to-understand medical information.

⚠️ This chatbot does NOT diagnose, prescribe, or replace a licensed doctor.

🚀 Live Demo

🔗 Streamlit App: your-app-url-here
🔗 GitHub Repository: this repo

📌 Features
✅ 1. PDF-Based RAG

Upload medical PDFs (guides, health articles, notes).

System extracts text from each PDF using PyPDF2.

Answers are grounded in retrieved content.

✅ 2. Groq LLM (Llama-3.1-8B-Instant)

Fast, reliable inference through Groq API.

Used for generating safe, simple, and structured answers.

✅ 3. Web Search (DuckDuckGo) – Optional

Provides fresh information from the internet.

Automatically summarized into the final answer.

✅ 4. Two Response Modes

Concise: 2–4 sentences

Detailed: Well-structured explanation with bullet points

✅ 5. Medical Safety Layer

No prescriptions

No diagnosis

Encourages doctor consultation

Emergency warning detection

🛠️ Tech Stack
Component	Technology
LLM	Groq – Llama-3.1-8B-Instant
Framework	Streamlit
RAG	TF-IDF (scikit-learn)
PDF Processing	PyPDF2
Web Search	DuckDuckGo Search
Deployment	Streamlit Cloud
📂 Folder Structure
project/
│
├── app.py
├── config/
│   └── config.py
├── models/
│   └── llm.py
├── utils/
│   ├── rag.py
│   ├── pdf_utils.py
│   └── web_search.py
├── requirements.txt
└── README.md

🔑 Environment Variables (Secrets)

In Streamlit Cloud → Settings → Secrets:

GROQ_API_KEY="your-key-here"


No secrets are stored in the repository.

▶️ How to Run Locally

Clone the repository

git clone https://github.com/yourusername/medical_chatbot.git
cd medical_chatbot


Create virtual environment

python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows


Install dependencies

pip install -r requirements.txt


Add environment variable

set GROQ_API_KEY="your-key-here"      # Windows
export GROQ_API_KEY="your-key-here"   # Mac/Linux


Run

streamlit run app.py

📘 How It Works (Short Explanation)

User uploads PDFs

Text is extracted and converted to embeddings using TF-IDF

Query → Retrieve relevant PDF chunks

Optional: Run DuckDuckGo search for extra context

All context is combined into a structured system prompt

Sent to Groq Llama-3.1-8B-Instant

The model generates a safe, helpful answer

🚨 Disclaimer

This chatbot is for educational purposes only.
It cannot:

Diagnose conditions

Prescribe medicines

Provide emergency instructions
Always consult a licensed doctor for personal medical advice.

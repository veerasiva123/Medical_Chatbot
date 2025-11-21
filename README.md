# 🩺 Medical Information Chatbot (Groq + PDF RAG)

An educational medical chatbot that uses **PDF-based retrieval**, **Groq Llama-3.1-8B-Instant**, and **DuckDuckGo web search** to provide simplified and reliable medical information.

⚠️ *This chatbot does NOT diagnose, prescribe medicines, or replace a licensed doctor.*

---

## 🔗 Live Links

<p>
👉 Open the <a href="https://medicalchatbot-39zwt8s5xoqymnf2ukxm3v.streamlit.app">Streamlit Medical Chatbot App</a>  
👉 View the <a href="https://github.com/veerasiva123/Medical_Chatbot">GitHub Repository</a>
</p>

---

## ⭐ Features

### 📄 1. PDF-Based RAG (Retrieval-Augmented Generation)
- Upload medical PDFs such as guides, articles, FAQs.
- Text is extracted and indexed using TF-IDF.
- Answers are grounded in PDF content.

### ⚡ 2. Fast LLM Responses (Groq)
- Model: **Llama-3.1-8B-Instant** via Groq API.
- Very fast response time.

### 🌐 3. DuckDuckGo Web Search (Optional)
- Fetches fresh external information.
- Summarized safely into the final answer.

### 📝 4. Two Response Styles
- **Concise** → Short 2–4 sentences  
- **Detailed** → Structured explanation with sections/bullets  

### 🛡 5. Medical Safety Rules
- No medical diagnosis  
- No prescriptions  
- Encourages doctor consultation  
- Emergency symptom detection  

---

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| LLM | Groq – Llama-3.1-8B-Instant |
| Framework | Streamlit |
| RAG | TF-IDF (scikit-learn) |
| PDF Extraction | PyPDF2 |
| Web Search | DuckDuckGo Search |
| Deployment | Streamlit Cloud |

---

## 📂 Project Structure

project/
│
├── app.py
├── config/
│ └── config.py
├── models/
│ └── llm.py
├── utils/
│ ├── rag.py
│ ├── pdf_utils.py
│ └── web_search.py
├── requirements.txt
└── README.md

## 🔑 API Key (Secrets)

Add this in **Streamlit → App Settings → Secrets**:

GROQ_API_KEY="your-key-here"

yaml
Copy code

Do NOT store your key inside the repo.

---

## ▶️ Run Locally

### 1. Clone the repo  
```sh
git clone https://github.com/veerasiva123/Medical_Chatbot
cd Medical_Chatbot
2. Create virtual environment
sh
Copy code
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
3. Install dependencies
sh
Copy code
pip install -r requirements.txt
4. Add your environment variable
sh
Copy code
set GROQ_API_KEY="your-key-here"      # Windows
export GROQ_API_KEY="your-key-here"   # Mac/Linux
5. Run
sh
Copy code
streamlit run app.py
📘 How It Works
User uploads PDFs

Text is extracted using PyPDF2

TF-IDF retrieves relevant segments

Optional DuckDuckGo search adds context

Combined prompt → Groq generates answer

Output is simplified + safety-filtered

📜 Disclaimer
This chatbot provides general educational medical information only.
It cannot diagnose, treat, or give emergency instructions.
Always consult a licensed doctor for medical concerns.

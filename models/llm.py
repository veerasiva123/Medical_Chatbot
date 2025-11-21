from typing import List, Dict
from dataclasses import dataclass
import requests
from config import config

GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"


@dataclass
class LLMClient:
    temperature: float = 0.2

    def __post_init__(self):
        if not config.GROQ_API_KEY or not config.GROQ_API_KEY.startswith("gsk_"):
            raise RuntimeError("GROQ_API_KEY is not set correctly. Edit config/config.py and add your key.")

    def chat(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for m in messages:
            role = m.get("role", "user")
            if role not in ("user", "assistant", "system"):
                role = "user"
            formatted_messages.append({"role": role, "content": m.get("content", "")})

        payload = {
            "model": config.GROQ_CHAT_MODEL,
            "messages": formatted_messages,
            "temperature": float(self.temperature),
        }

        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(GROQ_API_BASE, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise RuntimeError(f"HTTP request to Groq failed: {e}")

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            raise RuntimeError(f"Unexpected Groq response: {data}")
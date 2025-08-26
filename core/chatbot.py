# core/chatbot.py
import requests, hashlib
from .prompts import build_role_prompt
from .utils import load_all_records

class HiringChatbot:
    def __init__(self, model: str = "mistral:latest", language: str = "en"):
        self.model = model
        self.language = language
        self.base_url = "http://localhost:11434/api/generate"

    def generate_questions(self, candidate: dict, n: int = 5):
        prompt = build_role_prompt(candidate, num_questions=n)
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60
            )
            response.raise_for_status()
            text = response.json()["response"].strip()
            return [q.lstrip("1234567890). ").strip() for q in text.split("\n") if q.strip()][:n]
        except Exception as e:
            print("Ollama LLM failed:", e)
            return [
                f"What motivated you to apply for the role of {candidate.get('role')}?",
                f"Describe a challenge you faced in your {candidate.get('years_exp')} years of experience relevant to this role.",
                f"What key strengths make you a good fit for {candidate.get('role')}?",
                f"How do you stay updated with industry trends in {candidate.get('role')}?",
                "Where do you see yourself in 5 years?"
            ]

    def chat_reply(self, conversation: list) -> str:
        # Concatenate conversation into a single text prompt
        conv_text = ""
        for msg in conversation:
            role = msg["role"]
            content = msg["content"]
            conv_text += f"{role.upper()}: {content}\n"
        conv_text += "ASSISTANT:"

        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": conv_text, "stream": False},
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            print("Ollama chat failed:", e)
            last_user = [m for m in conversation if m["role"] == "user"][-1]["content"]
            return f"(Fallback) I understood: {last_user}. Can you elaborate?"

    def match_prior(self, email: str):
        records = load_all_records()
        h = hashlib.sha256(email.lower().encode()).hexdigest()
        for rid, rec in records.items():
            if rec.get("email_hash") == h:
                return {"id": rid, "summary": rec.get("summary", "Found previous record")}
        return None

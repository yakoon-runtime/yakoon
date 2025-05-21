import os
from dataclasses import dataclass


@dataclass
class Settings:
    backend: str = os.getenv("YAKOON_AI_BACKEND", "ollama")
    model: str = os.getenv("YAKOON_GPT_MODEL", "gpt-4")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    time_out: str = 60.0

settings = Settings()

import httpx
from yakoon.saas.plugins.ai.settings import Settings


async def ask_ollama(prompt: str, context: dict = {}) -> str:
    payload = {
        "model": context.get("model", "mistral"),
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=Settings.time_out) as client:
        response = await client.post(Settings.ollama_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
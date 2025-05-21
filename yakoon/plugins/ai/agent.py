
from yakoon.plugins.ai.settings import Settings


async def ask_AI(prompt: str, context: dict = {}) -> str:

    backend = Settings.backend 
    if backend == "openai":
        from yakoon.plugins.ai.agent_openai import ask_openai
        return await ask_openai(prompt, context)
    elif backend == "ollama":
        from yakoon.plugins.ai.agent_ollama import ask_ollama
        return await ask_ollama(prompt, context)
    else:
        raise RuntimeError(f"Unbekannter AI-Backend: {backend}")
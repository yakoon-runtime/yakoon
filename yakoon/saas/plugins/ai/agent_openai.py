
from yakoon.saas.plugins.ai.settings import Settings


async def ask_openai(prompt: str, context: dict = {}) -> str:

    try:
        import openai
        openai.api_key = Settings.openai_api_key
    except:
        raise RuntimeError(f"Open AI not installed.")
    
    model = context.get("model", "gpt-4")
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

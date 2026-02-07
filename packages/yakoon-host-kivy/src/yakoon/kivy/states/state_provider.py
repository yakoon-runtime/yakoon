
from dataclasses import dataclass

@dataclass(frozen=True)
class UIState:
    prompt_prefix: str
    prompt_secret: bool


class UIStateProvider:

    def __init__(self, session):
        self.session = session

    def __call__(self) -> UIState:
        prompt = getattr(self.session, "prompt_prefix", "stefan@app$")
        secret = getattr(self.session, "prompt_secret", False)
        return UIState(prompt_prefix=prompt, prompt_secret=secret)

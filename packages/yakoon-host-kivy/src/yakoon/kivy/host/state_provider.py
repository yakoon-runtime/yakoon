
class UIStateProvider:

    def __init__(self, session):
        self.session = session

    def __call__(self):
        prompt = getattr(self.session, "prompt_prefix", "stefan@app$")
        secret = getattr(self.session, "prompt_secret", False)
        return {"prompt_prefix": prompt, "prompt_secret": secret}
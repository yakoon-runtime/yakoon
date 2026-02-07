from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from pathlib import Path
from kivy.app import App

from yakoon.kivy.utils.loader import load_layouts
from yakoon.kivy.pages.app_root import AppRootPage

from yakoon.kivy.host.app_controller import AppController
from yakoon.kivy.host.output import KivyOutput
from yakoon.kivy.host.runner import SessionRunner

# Demo
from yakoon.kivy.demo.engine import DemoEngine
from yakoon.kivy.demo.session import DemoSession

# wichtig: Widgets registrieren, bevor KV geladen wird (Factory.register etc.)
from yakoon.kivy import pages, widgets  # noqa: F401
from yakoon.kivy.utils import fonts     # noqa: F401

class YakoonKivyApp(App):

    def build(self):
        package_root = Path(__file__).resolve().parent
        load_layouts(package_root)

        root = AppRootPage()
        controller = AppController(root)

        engine = DemoEngine()
        session = DemoSession()

        # UI-State Provider (PromptPrefix etc.) – später aus Session/Controller ableiten
        def ui_state():
            # Beispiel: dynamischer Prompt
            prompt = getattr(session, "prompt_prefix", "stefan@app$")
            return {"prompt_prefix": prompt, "prompt_secret": False}

        session.bind_io(
            KivyOutput(session=session, 
                       dispatch_context=controller.dispatch_context, 
                       ui_state_provider=ui_state))

        runner = SessionRunner(engine, session)
        runner.start()

        # ChatWidget braucht runner für submit()
        root.ids.chat_widget.runner = runner

        # Fokus initial (wie du es willst)
        root.focus_initial()

        return root


if __name__ == "__main__":
    YakoonKivyApp().run()

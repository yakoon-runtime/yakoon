from kivy.config import Config

from yakoon.kivy.host.output_adapter import OutputAdapter
from yakoon.kivy.host.state_provider import UIStateProvider
from yakoon.platform.output.default import Output
Config.set('kivy', 'exit_on_escape', '0')

from pathlib import Path
from kivy.app import App

from yakoon.kivy.utils.loader import load_layouts
from yakoon.kivy.pages.app_root_page import AppRootPage

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

        engine = DemoEngine()
        session = DemoSession()

        root = AppRootPage()
        controller = AppController(root)

        # UI-State Provider (PromptPrefix etc.) – später aus Session/Controller ableiten
        def ui_state():
            # Beispiel: dynamischer Prompt
            prompt = getattr(session, "prompt_prefix", "stefan@app$")
            return {"prompt_prefix": prompt, "prompt_secret": False}

        ui_state_provider = UIStateProvider(session)
        kivy_out = KivyOutput(
            session, 
            controller.dispatch_context, 
            ui_state_provider=ui_state_provider)

        # Wichtig: Engine erwartet Output-Adapter, nicht KivyOutput direkt
        session.bind_io(OutputAdapter(
            emit_fn=kivy_out.emit,
            emit_err_fn=kivy_out.emit,
        ))

        runner = SessionRunner(engine, session)
        runner.start()

        controller.set_runner(runner)
        controller.new_chat_tab(select=True)

        # ChatWidget braucht runner für submit()
        #root.ids.chat_widget.runner = runner

        # Fokus initial (wie du es willst)
        root.focus_initial()

        return root


if __name__ == "__main__":
    YakoonKivyApp().run()

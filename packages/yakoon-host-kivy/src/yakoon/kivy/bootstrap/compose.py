from __future__ import annotations
from dataclasses import dataclass

from yakoon.kivy.bootstrap.dispatcher import ContextDispatcher
from yakoon.kivy.runtime.demo.engine import DemoEngine
from yakoon.kivy.runtime.demo.session import DemoSession
from yakoon.kivy.runtime.output import OutputAdapter, KivyOutput
from yakoon.kivy.runtime.runner import SessionRunner
from yakoon.kivy.pages.app_root_page import AppRootPage
from yakoon.kivy.controllers.app_controller import AppController
from yakoon.kivy.states.state_provider import UIStateProvider


@dataclass
class KivyComposition:
    root: AppRootPage
    controller: AppController
    runner: SessionRunner
    output: KivyOutput
    dispatcher: ContextDispatcher
    session: object
    engine: object


def compose_kivy_app() -> KivyComposition:

    # 2) Domain
    engine = DemoEngine()
    session = DemoSession()

    # 3) UI root + dispatcher
    root = AppRootPage()
    dispatcher = ContextDispatcher()

    # 4) Output (kann dispatcher schon nutzen)
    output = KivyOutput(
        session=session,
        on_context=dispatcher,
        ui_state_provider=UIStateProvider(session)
    )

    # 5) OutputAdapter -> Session
    session.bind_io(OutputAdapter(
        emit_fn=output.emit,
        emit_err_fn=output.emit,
    ))

    # 6) Runner
    runner = SessionRunner(engine, session)

    # 7) Controller
    controller = AppController(root, runner)
    # 8) Jetzt verdrahten wir Output -> Controller
    dispatcher.set_handler(controller.dispatch_context)

    # 9) Start
    runner.start()
    controller.new_chat_tab(select=True)

    return KivyComposition(
        root=root,
        controller=controller,
        runner=runner,
        output=output,
        dispatcher=dispatcher,
        session=session,
        engine=engine,
    )

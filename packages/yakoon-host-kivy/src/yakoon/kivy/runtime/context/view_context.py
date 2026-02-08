from dataclasses import dataclass
from yakoon.kivy.states.state_provider import UIStateProvider
from yakoon.kivy.models.envelope import Envelope


@dataclass
class ViewContext:
    session: object
    envelope: Envelope
    ui_state_provider: callable  # returns UIState

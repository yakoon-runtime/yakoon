from dataclasses import dataclass
from yakoon.kivy.host.state_provider import UIStateProvider
from yakoon.kivy.models.envelope import Envelope


@dataclass
class ViewContext:
    session: object
    envelope: Envelope
    ui_state: UIStateProvider

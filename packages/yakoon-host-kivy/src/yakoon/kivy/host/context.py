from dataclasses import dataclass
from yakoon.kivy.models.envelope import Envelope


@dataclass
class ViewContext:
    session: object
    envelope: Envelope
    ui_state: dict

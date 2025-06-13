
from dataclasses import dataclass

from .render import RenderSettings
from .logging import LoggingSettings
from .network import NetSettings
from .base import BaseSettings


@dataclass
class MeshSettings:

    base = BaseSettings()
    logging = LoggingSettings()
    network = NetSettings()
    render = RenderSettings()

settings = MeshSettings()



from dataclasses import dataclass

from .render import RenderSettings
from .logging import LoggingSettings
from .network import NetSettings
from .base import BaseSettings
from .loop import LoopSettings


@dataclass
class MeshSettings:

    base = BaseSettings()
    logging = LoggingSettings()
    network = NetSettings()
    render = RenderSettings()
    loop = LoopSettings()

settings = MeshSettings()


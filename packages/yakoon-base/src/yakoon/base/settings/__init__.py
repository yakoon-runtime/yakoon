
from dataclasses import dataclass
from .base import BaseSettings


@dataclass
class MeshSettings:

    base = BaseSettings()

settings = MeshSettings()


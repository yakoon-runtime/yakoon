
import os
from dataclasses import dataclass

from yakoon.base.runtime.render.models.mode import RenderMode


@dataclass
class RenderSettings:

    render_mode = RenderMode.MARKDOWN

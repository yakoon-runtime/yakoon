
import os
from dataclasses import dataclass

from yakoon.platform.runtime.render.mode import RenderMode


@dataclass
class RenderSettings:

    render_mode = RenderMode.MARKDOWN

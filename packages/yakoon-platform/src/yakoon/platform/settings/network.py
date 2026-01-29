
import os
from dataclasses import dataclass


@dataclass
class NetSettings:

    prompt_timed_out = 30
    """Timeout in seconds. If reached, the prompt is cancelled."""

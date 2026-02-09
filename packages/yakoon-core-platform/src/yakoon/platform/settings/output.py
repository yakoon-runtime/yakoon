
import os
from dataclasses import dataclass

from yakoon.base.models.format import OutputFormat


@dataclass
class OutputSettings:

    format = OutputFormat.PLAIN

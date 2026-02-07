from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class TabState:
    tabs: list[dict] = field(default_factory=list)          # [{"id": str, "title": str}, ...]
    pages: dict[str, Any] = field(default_factory=dict)     # tab_id -> page/widget
    active_tab_id: Optional[str] = None
    counter: int = 0

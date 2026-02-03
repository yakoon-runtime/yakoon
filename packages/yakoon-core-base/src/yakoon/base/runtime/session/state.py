from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime, timezone


@dataclass
class SessionState:
    last_active: datetime | None = None
    active_controller_id: Optional[str] = None
    account_key: Optional[str] = None
    username: Optional[str] = None
    data: Dict[str, Any] = None         # bewusst "misc", wenn du es willst

    def to_dict(self) -> dict:
        d = asdict(self)
        if d["data"] is None:
            d["data"] = {}
        if self.last_active:
            d["last_active"] = self.last_active.astimezone(timezone.utc).isoformat()
        else:
            d["last_active"] = None

        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SessionState":
       d = dict(d or {})
       d.setdefault("data", {})
       raw_last_active = d.pop("last_active", None)
       obj = cls(**d)
       if raw_last_active:
           obj.last_active = datetime.fromisoformat(raw_last_active)

       return obj



class SessionRuntime:
    
    def __init__(self):
        self.data: dict[str, object] = {}
        self.signals: set[str] = set()
        self.io = None   

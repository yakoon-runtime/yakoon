
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from yakoon.runtime.models.session import BaseSession
from yakoon.domains.platform.models.account import Account


@dataclass
class PlatformSession(BaseSession):

    # ───── persistent fields (stored in DB/json) ─────

    account_id: str = field(default=None)
    permissions: list[str] = field(default_factory=lambda: ["system"])
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ───── transient runtime-only attributes ─────

    _account: Optional[Account] = field(default=None, init=False, repr=False)

        
    @property
    def is_anonymous(self) -> bool:
        return self.account_id is None

    @property
    def account(self) -> Account | None:
        return self._account

    @account.setter
    def account(self, value):
        self._account = value



from yakoon.runtime.models.session import BaseSession


class Secured:
    editable_by: list[str] = []  # z. B. ["admin"]
    deletable_by: list[str] = []  # z. B. ["builder"]
    viewable_by: list[str] = []  # z. B. ["player", "admin"]

    def has_perm(self, session: BaseSession, action: str) -> bool:
        perms = {
            "edit": self.editable_by,
            "delete": self.deletable_by,
            "view": self.viewable_by
        }.get(action, [])

        return any(p in session.permissions for p in perms)

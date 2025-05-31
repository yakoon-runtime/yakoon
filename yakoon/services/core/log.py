from yakoon.engine.settings import Settings


class LogService:
    
    @classmethod
    def audit(cls, msg: str):
        if Settings.log_commands:
            print(f"[AUDIT] {msg}")

    @classmethod
    def error(cls, exc: Exception):
        if Settings.log_errors:
            import traceback
            print("[ERROR]", "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

    @classmethod
    def permission(cls, session, obj, action):
        if Settings.log_permission_denied:
            print(f"[SEC] Denied: {session.id} → {obj} ({action})")

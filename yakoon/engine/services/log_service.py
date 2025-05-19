# yakoon/engine/services/log_service.py

from yakoon.engine.settings import settings


class LogService:
    
    @staticmethod
    def audit(msg: str):
        if settings.get("log_commands"):
            print(f"[AUDIT] {msg}")

    @staticmethod
    def error(exc: Exception):
        if settings.get("log_errors"):
            import traceback
            print("[ERROR]", "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

    @staticmethod
    def permission(session, obj, action):
        if settings.get("log_permission_denied"):
            print(f"[SEC] Denied: {session.id} → {obj} ({action})")

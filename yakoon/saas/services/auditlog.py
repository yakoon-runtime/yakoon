from yakoon.saas.engines.command.settings import Settings


class AuditLogService:
    
    async def audit(self, msg: str):
        if Settings.log_commands:
            print(f"[AUDIT] {msg}")

    async def error(self, exc: Exception):
        if Settings.log_errors:
            import traceback
            print("[ERROR]", "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))

    async def permission(self, session, obj, action):
        if Settings.log_permission_denied:
            print(f"[SEC] Denied: {session.key} → {obj} ({action})")

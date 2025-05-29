from dataclasses import dataclass
from yakoon.engine.settings import Settings as BaseSettings
from yakoon.platform.render.engine.mode import RenderMode


@dataclass
class RuntimeSettings:
    render_mode: str = RenderMode.MARKDOWN


class Settings(BaseSettings):

    runtime: RuntimeSettings = RuntimeSettings()

    # Debugging & Logging
    debug: bool = False
    """If True, enables verbose output and developer diagnostics."""

    # Feature Toggles
    enable_batch: bool = False
    """Allows multiple commands in one input via 'batch:' prefix."""

    cmd_category_account: str = "account"
    """Commands related to login, logout, and account creation. Typically available before authentication."""

    cmd_category_system: str = "system"
    """General-purpose system commands like @who or @switch. Usually accessible with or without login."""

    cmd_category_admin: str = "admin"
    """Administrative commands such as user creation, shutdown, or platform configuration. Requires elevated rights."""

    cmd_category_workspace: str = "workspace"
    """Commands for productive domain-specific actions, such as creating invoices or navigating rooms."""

    cmd_category_debug: str = "debug"
    """Development-only commands used for testing, diagnostics, or inspection."""
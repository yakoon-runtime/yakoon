# yakoon/engine/settings.py

from dataclasses import dataclass

@dataclass
class Settings:
    """
    Core configuration for the Yakoon engine.
    Can be extended or overridden by project-specific settings.
    """

    # Debugging & Logging
    debug: bool = True
    """If True, enables verbose output and developer diagnostics."""

    log_commands: bool = True
    """Logs every command issued by a session."""

    log_errors: bool = True
    """Logs unexpected exceptions raised during execution."""

    log_permission_denied: bool = True
    """Logs access denials (e.g. PermissionError, has_perm=False)."""

    log_to_file: bool = False
    """If True, logs will also be written to a file."""

    log_file_path: str = "yakoon.log"
    """Path to the log file if log_to_file is enabled."""

    # Feature Toggles
    enable_batch: bool = True
    """Allows multiple commands in one input via 'batch:' prefix."""

    enable_webapi: bool = True
    """Enables the FastAPI-based web interface."""

    enable_telnet: bool = True
    """Enables the Telnet server interface."""

# Global settings instance used throughout the engine
settings = Settings()

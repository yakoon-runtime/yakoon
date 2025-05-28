from yakoon.engine.settings import Settings as BaseSettings


class Settings(BaseSettings):

    # Debugging & Logging
    debug: bool = False
    """If True, enables verbose output and developer diagnostics."""

    # Feature Toggles
    enable_batch: bool = False
    """Allows multiple commands in one input via 'batch:' prefix."""

    # Time & Realm Loop
    tick_rate: float = 60.0
    """Number of real-time seconds per realm tick (default = 60s)."""
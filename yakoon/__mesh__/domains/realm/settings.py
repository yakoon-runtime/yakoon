

class Settings():

    # Debugging & Logging
    debug: bool = False
    """If True, enables verbose output and developer diagnostics."""

    # Time & Realm Loop
    tick_rate: float = 60.0
    """Number of real-time seconds per realm tick (default = 60s)."""
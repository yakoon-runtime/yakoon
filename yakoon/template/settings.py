from yakoon.engine.settings import settings as base


settings = base.copy()
settings["debug"] = False
settings["log_to_file"] = True

from .engine import EngineSettings
from .plugings import AISettings
from .cmdsets import CmdSetCategoriesSetting

class SaasSettings:

    ai = AISettings()
    engine = EngineSettings()
    cmdsets = CmdSetCategoriesSetting()


settings = SaasSettings()
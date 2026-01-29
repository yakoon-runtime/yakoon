from yakoon.platform.settings.cmdsets import CmdSetCategoriesSetting
from yakoon.platform.settings.engine import EngineSettings
from yakoon.platform.settings.logging import LoggingSettings
from yakoon.platform.settings.network import NetSettings
from yakoon.platform.settings.plugings.ai import AISettings
from yakoon.platform.settings.render import RenderSettings

class SaasSettings:

    ai = AISettings()
    engine = EngineSettings()
    network = NetSettings()
    logging = LoggingSettings()
    render = RenderSettings()

    cmdsets = CmdSetCategoriesSetting()


settings = SaasSettings()
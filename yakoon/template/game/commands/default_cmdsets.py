from typing import Sequence, Type
from yakoon.engine.core.command import Command


from yakoon.game.commands.account.login.cmdset import LoginAccountCommands as _LAC
class LoginAccountCommands(_LAC):
    
    #mode = "login"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]


from yakoon.game.commands.account.general.cmdset import GeneralAccountCommands as _GAC
class GeneralAccountCommands(_GAC):
    
    #mode = "account"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]
    

from yakoon.game.commands.character.general.cmdset import GeneralCharacterCommands as _GCC
class GeneralCharacterCommands(_GCC):
    
    #mode = "character"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]

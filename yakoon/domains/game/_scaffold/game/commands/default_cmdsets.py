from typing import Sequence, Type
from yakoon.engine.core.command import Command

# Commands: Account Login/Registration

from yakoon.domains.game.commands.account.login.cmdset import LoginAccountCommands as _LAC
class LoginAccountCommands(_LAC):
    """
    Commands available before login (e.g. register, connect)
    """

    #category = "login"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]


from yakoon.domains.game.commands.account.general.cmdset import GeneralAccountCommands as _GAC
class GeneralAccountCommands(_GAC):
    """
    Commands available to work in the account (e.g. createuser, password)
    """
    
    #category = "account"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]
    
# Commands: In-Game Character Use

from yakoon.domains.game.commands.character.general.cmdset import GeneralCharacterCommands as _GCC
class GeneralCharacterCommands(_GCC):
    """
    Commands available for the character (e.g. look, move, get)
    """
    
    #category = "character"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return super().commands() # + [ExtraCommand]

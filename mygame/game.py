from engine.core.game.definition import BaseGameDefinition
from mygame.commands.account.general.cmdset import GeneralAccountCommands
from mygame.commands.account.login.cmdset import LoginAccountCommands
from mygame.commands.character.general.cmdset import GeneralCharacterCommands
from mygame.runtime.session import GameSession


class GameDefinition(BaseGameDefinition):

    session_cls = GameSession
    """ Defines the game session object """

    default_command_groups = ["login"]     
    """ Defines the default command group"""

    commandsets = [
        LoginAccountCommands, 
        GeneralAccountCommands, 
        GeneralCharacterCommands]
    """ The collection of all commands. """
     
    async def on_before_run_command(session: GameSession, request, command):
        if required := getattr(command, "requires", []):
            if not set(required).issubset(set(session.permissions)):
                raise PermissionError(f"Du darfst das nicht tun. Erforderlich: {', '.join(required)}")
    
    async def on_after_run_command(session: GameSession, request, command):
        if session.account and not session.character: 
             session.ctx.router.unregister(session.id)
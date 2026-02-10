from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.workflow.commands.cmd_cancel import CmdWfCancel
from yakoon.workflow.commands.cmd_next import CmdWfNext
from yakoon.workflow.commands.cmd_prompt import CmdWfPrompt
from yakoon.workflow.commands.cmd_run import CmdWfRun



class ShellWorkflowCommands(CommandSet):
    
    group = "workflow"

    @classmethod
    def commands(cls) -> Sequence[Type[Command]]: 
        return [            
            CmdWfRun,
            CmdWfPrompt,
            CmdWfNext,
            CmdWfCancel,
        ]
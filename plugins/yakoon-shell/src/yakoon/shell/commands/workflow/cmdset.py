from typing import Sequence, Type
from yakoon.base.commands.command import Command
from yakoon.base.commands.commandset import CommandSet
from yakoon.shell.commands.workflow.cmd_cancel import CmdWfCancel
from yakoon.shell.commands.workflow.cmd_next import CmdWfNext
from yakoon.shell.commands.workflow.cmd_prompt import CmdWfPrompt
from yakoon.shell.commands.workflow.cmd_run import CmdWfRun


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
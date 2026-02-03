

from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.ports import CommandQueueService
from yakoon.base.runtime.session.session import Session


class WorkflowCommand(Command):
    """
    A command that schedules follow-up commands into the CommandQueueService.
    It does not execute them itself.
    """

    def schedule(self, session, commands: list[str]):
        queue = self.services.get(CommandQueueService)
        queue.enqueue_commands(session, commands)

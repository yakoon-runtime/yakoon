from yakoon.base.ports import AuditLogService
from yakoon.base.commands.command import Command
from yakoon.base.commands.request import Request
from yakoon.base.runtime.session import Session


class CmdSendMail(Command):

    key = "sendmail"

    async def run(self, session: Session, request: Request):

        presenter = await self.get_presenter(session)
        audits = self.services.get(AuditLogService)

        message = "Das ist mein Text"
        # message = await presenter.prompts.ask("message")

        await audits.audit(f"Mail sent: {message}")
        await presenter.emit("mail_sent", message=message)

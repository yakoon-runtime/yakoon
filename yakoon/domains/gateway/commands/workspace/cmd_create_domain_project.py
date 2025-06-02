import importlib
from pathlib import Path
from yakoon.commands.command import Command
from yakoon.commands.parser import Request
from yakoon.domains.gateway.runtime.session import GatewaySession

"""
 subcommands -> Der parser kann das....

        self.cmd = ""
        self.subcmd = ""
        self.switches = []
        self.args = []
        self.kwargs = {}

"""

class CmdCreateDomainProject(Command):
    """
    create project domain=realm name=minddojo
    """

    key = "create"

    async def run(self, session: GatewaySession, request: Request):
        
        domain = request.kwargs.get("domain")
        name = request.kwargs.get("name")

        if not domain or not name:
            raise ValueError("Bitte gib domain=<name> und name=<projektname> an.")

        try:
            # Lade scaffold-Modul der Domain
            scaffold_mod = importlib.import_module(f"yakoon.domains.{domain}.scaffold")
        except ModuleNotFoundError:
            raise ValueError(f"Unbekannte Domain: {domain}")

        # Zielpfad
        target_path = Path(name).resolve()

        try:
            scaffold_mod.create_project(target_path, name)
        except Exception as e:
            raise ValueError(f"Fehler beim Erstellen: {e}")

        await session.emit(f"✅ Domain-Projekt '{name}' aus '{domain}' erstellt unter: {target_path}")

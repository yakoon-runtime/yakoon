import importlib
from pathlib import Path
from yakoon.platform.commands.command import SaasCommand
from yakoon.base.commands.parser import Request
from yakoon.base.runtime.session import BaseSession

"""
 subcommands -> Der parser kann das....

        self.cmd = ""
        self.subcmd = ""
        self.switches = []
        self.args = []
        self.kwargs = {}

"""

class CmdCreateDomainProject(SaasCommand):
    """
    create project domain=realm name=minddojo
    """

    key = "create"

    async def run(self, session: BaseSession, request: Request):
        
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

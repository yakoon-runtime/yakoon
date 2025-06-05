# yakoon/cli.py

import typer
import asyncio
import sys
    
from yakoon.apps.yakoon.utils.migrate import migrate_from_config


cli = typer.Typer()


@cli.command()
def testme(foo: str = typer.Option(...)):
    print(f"FOO is: {foo}")

    
@cli.command()
def migrate(config: str = typer.Option(..., help="Path to store config YAML")):
    """
    Run all registered domain migrations based on the given config.
    """
    asyncio.run(migrate_from_config(config))


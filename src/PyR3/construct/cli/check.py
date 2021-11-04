# -*- coding: utf-8 -*-

import click
from click.types import Path
from rich.console import Console

from PyR3.construct.cli.const import EXIT_CODE
from PyR3.construct.mp import MeshProject, ProjectComponent

CONSOLE = Console()


@click.argument(
    "project_path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
def check(project_path: Path):
    EXIT_CODE.COMPONENT_WITH_SYMBOL_EXISTS
    MeshProject
    ProjectComponent

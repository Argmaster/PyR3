# -*- coding: utf-8 -*-
from pathlib import Path

import click
from rich.console import Console

from PyR3.construct.mp import MeshProject

CONSOLE = Console()


@click.argument("project_name")
@click.argument("save_path", type=Path)
def new(project_name: str, save_path: Path):
    MeshProject(
        project_file_path=save_path,
        format_version="1.0.0",
        project_version="1.0.0",
        project_name=project_name,
        description="",
        scale=1.0,
        component_list=[],
    ).dump()
    CONSOLE.print(
        f"Created Mesh Project file '{save_path.resolve()}'.", style="green"
    )

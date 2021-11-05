# -*- coding: utf-8 -*-
from pathlib import Path

import click
from rich.console import Console

from PyR3.construct.cli.const import EXIT_CODE
from PyR3.construct.mp import MeshProject

CONSOLE = Console()


@click.argument("project_name")
@click.argument("save_path", type=Path)
@click.option("--force", "-f", is_flag=True)
def new(project_name: str, save_path: Path, force: bool):
    if not force and save_path.exists():
        CONSOLE.print(
            f"File '{save_path}' already exists, use -f flag to overwrite it.",
            style="red",
        )
        exit(EXIT_CODE.FILE_EXISTS)
    else:
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
            f"Created Mesh Project file '{save_path.resolve()}'.",
            style="green",
        )

# -*- coding: utf-8 -*-
from pathlib import Path

import click
from rich.console import Console

from PyR3.construct.parse_place import PlaceFile

CONSOLE = Console()


@click.argument("place_path", type=Path)
@click.argument("save_path", type=Path)
def from_place(place_path: Path, save_path: Path):
    PlaceFile.load(place_path).to_MeshProject().dump(save_path)
    CONSOLE.print(
        f"Created Mesh Project file '{save_path.resolve()}'.", style="green"
    )

# -*- coding: utf-8 -*-
from typing import Tuple

import click
from rich.console import Console

from PyR3.construct.cli.const import EXIT_CODE
from PyR3.construct.mp import ProjectComponent

from .check import load_mesh_project

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
@click.argument("symbol")
@click.argument("x", type=float)
@click.argument("y", type=float)
@click.argument("tags", nargs=-1)
@click.option("--hash", default="")
@click.option("--version", default="1.0.0")
@click.option("--rotation", default=0.0)
@click.option("--is_top", default=True)
def add(
    project_path: str,
    symbol: str,
    x: float,
    y: float,
    tags: Tuple[str],
    **kwargs,
):
    mesh_project = load_mesh_project(project_path)
    _validate_unique_symbol(symbol, mesh_project)
    mesh_project.component_list.append(
        ProjectComponent(
            symbol=symbol,
            x=x,
            y=y,
            tags=list(tags),
            **kwargs,
        )
    )
    mesh_project.dump()


def _validate_unique_symbol(symbol, mesh_project):
    for component in mesh_project.component_list:
        if component.symbol == symbol:
            CONSOLE.print(
                f"Component with symbol {symbol} already contained in project."
            )
            exit(EXIT_CODE.COMPONENT_WITH_SYMBOL_EXISTS)

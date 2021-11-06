# -*- coding: utf-8 -*-

import click

from .add import add
from .check import check
from .const import CONSOLE
from .from_place import from_place
from .new import new


@click.group()
@click.option(
    "--no-rich",
    is_flag=True,
    help="Disable rich output (color tags, formatting).",
)
def main(no_rich: bool):
    if no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
        CONSOLE.print("Rich text disabled.", style="red")


new = main.command(help="Create new mesh project.")(new)
add = main.command(help="Create new mesh project.")(add)
check = main.command(help="Create new mesh project.")(check)
from_place = main.command(help="Create new mesh project.")(from_place)

# -*- coding: utf-8 -*-

import click
from rich.console import Console

from .add import add
from .from_place import from_place
from .new import new

CONSOLE = Console()


@click.option("--no-rich", "-r", is_flag=True, default=False, flag_value=True)
@click.group()
def main(no_rich: bool):
    if no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
        CONSOLE.print("Rich text disabled.", style="red")


new = main.command(help="Create new mesh project.")(new)
add = main.command(help="Create new mesh project.")(add)
from_place = main.command(help="Create new mesh project.")(from_place)

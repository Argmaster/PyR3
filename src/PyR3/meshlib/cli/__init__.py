# -*- coding: utf-8 -*-

import click
from rich.console import Console

from .add import add
from .mklib import mklib

CONSOLE = Console()


@click.option("--no-rich", "-r", is_flag=True, default=False, flag_value=True)
@click.group()
def main(no_rich: bool):
    if no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
        CONSOLE.print("Rich text disabled.", style="red")


mklib = main.command(help="Create new empty library.")(mklib)


add = main.command(help="Add model to existing library.")(add)

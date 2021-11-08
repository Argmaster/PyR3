# -*- coding: utf-8 -*-

import click
from rich.console import Console

from .add import add
from .mklib import mklib

CONSOLE = Console()


@click.group()
def main():
    pass


mklib = main.command(help="Create new empty library.")(mklib)
add = main.command(help="Add model to existing library.")(add)

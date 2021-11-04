# -*- coding: utf-8 -*-

import click

from .add import add
from .check import check
from .from_place import from_place
from .new import new


@click.group()
def main():
    pass


new = main.command(help="Create new mesh project.")(new)
add = main.command(help="Create new mesh project.")(add)
check = main.command(help="Create new mesh project.")(check)
from_place = main.command(help="Create new mesh project.")(from_place)

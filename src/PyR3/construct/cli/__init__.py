# -*- coding: utf-8 -*-

from PyR3.const import common_main

from .add import add
from .check import check
from .from_place import from_place
from .new import new

new = common_main.command(help="Create new mesh project.")(new)
add = common_main.command(help="Add component to existing project.")(add)
check = common_main.command(help="Check project validity.")(check)
from_place = common_main.command(help="Create new project from place file.")(
    from_place
)

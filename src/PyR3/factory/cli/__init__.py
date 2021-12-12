# -*- coding: utf-8 -*-
from PyR3.const import common_main

from .build import build

build = common_main.command(help="Build a 3D model from model specification.")(
    build
)

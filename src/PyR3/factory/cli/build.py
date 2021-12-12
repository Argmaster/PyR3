# -*- coding: utf-8 -*-
from pathlib import Path

import click

from PyR3.factory import build_from_file


@click.argument("cfg_file", type=Path)
@click.argument("save_file", type=Path)
def build(cfg_file: Path, save_file: Path):
    build_from_file(cfg_file, save_file)

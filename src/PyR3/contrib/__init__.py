# -*- coding: utf-8 -*-


from pathlib import Path

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to


def build_and_save(class_: type, params: dict, save_path: Path):
    wipeScenes()
    class_(params).render()
    print(save_path)
    export_to(filepath=save_path)

# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import toml
import yaml

from PyR3.meshlib.lib_obj.model_info import ModelInfoBase

from .lib_info import LibraryInfoBase, LibraryInfoV1_0_0


def load(lib_file_path: str) -> LibraryObject:
    with open(lib_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return LibraryObject(Path(lib_file_path), **data)


def dump(ob: LibraryObject | LibraryInfoBase | ModelInfoBase, lib_file_path: str):
    with open(lib_file_path, "w", encoding="utf-8") as file:
        yaml.dump(ob.dict(), file, indent=2, allow_unicode=True, sort_keys=False)


class LibraryObject:

    INFO_VERSION_MAPPING = {"1.0.0": LibraryInfoV1_0_0}
    lib_file_path: Path
    info: LibraryInfoBase

    def __init__(self, lib_file_path: Path, *, version: str, **kwargs) -> None:
        self.lib_file_path = lib_file_path
        self.version = version
        InfoClass = self._get_InfoClass()
        self.info = InfoClass(
            lib_file_path=self.lib_file_path,
            **kwargs,
        )

    def save_in_place(self):
        dump(self, self.lib_file_path)

    def dict(self):
        return self.info.dict()

    def _get_InfoClass(self):
        InfoClass = self.INFO_VERSION_MAPPING.get(self.version, None)
        if InfoClass is None:
            raise TypeError(
                f"LibraryInfoV{self.version.replace('.', '_')} not supported."
            )
        return InfoClass

    def __eq__(self, o: LibraryObject) -> bool:
        return isinstance(o, LibraryObject) and self.info == o.info

    def __str__(self) -> str:
        return f'Library[{self.info} at "{self.lib_file_path}"]'

    __repr__ = __str__

# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import toml
import yaml

from .lib_info import LibraryInfoBase, LibraryInfoV1_0_0


def load(lib_file_path: str) -> LibraryObject:
    extension = Path(lib_file_path).suffix
    if extension in (".yml", ".yaml"):
        loader = yaml.safe_load
    elif extension in (".json"):
        loader = json.load
    elif extension in (".toml"):
        loader = toml.load
    else:
        raise TypeError(f"Failed to recognize file format from extension {extension}.")
    with open(lib_file_path) as file:
        data = loader(file.read())
    return LibraryObject(lib_file_path, **data)


def dump(ob: LibraryObject, lib_file_path: str):
    extension = Path(lib_file_path).suffix
    if extension in (".yml", ".yaml"):
        serializer = yaml.safe_dump
    elif extension in (".json"):
        serializer = json.dump
    elif extension in (".toml"):
        serializer = toml.dump
    else:
        raise TypeError(f"Failed to recognize file format from extension {extension}.")
    with open(lib_file_path, "w", encoding="utf-8") as file:
        serializer(ob, file)


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

    def _get_InfoClass(self):
        InfoClass = self.INFO_VERSION_MAPPING.get(self.version, None)
        if InfoClass is None:
            raise ValueError(
                f"LibraryInfoV{self.version.replace('.', '_')} not supported."
            )
        return InfoClass

    def __str__(self) -> str:
        return f'Library["{self.lib_file_path}" {self.info}]'

    __repr__ = __str__

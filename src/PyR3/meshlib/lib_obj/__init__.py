# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import toml
import yaml

from .lib_info import LibraryInfoBase, LibraryInfoV1_0_0


def load(path: str) -> LibraryObject:
    extension = Path(path).suffix
    with open(path) as file:
        if extension in (".yml", ".yaml"):
            data = yaml.safe_load(file)
        elif extension in (".json"):
            data = json.load(file)
        elif extension in (".toml"):
            data = toml.load(file)
        else:
            raise TypeError(
                f"Failed to recognize file format with extension {extension}."
            )
    return LibraryObject(path, **data)


class LibraryObject:

    INFO_VERSION_MAPPING = {"1.0.0": LibraryInfoV1_0_0}
    lib_file_path: str
    info: LibraryInfoBase

    def __init__(self, lib_file_path: str, *, version: str, **kwargs) -> None:
        self.lib_file_path = Path(lib_file_path)
        info_class = self.INFO_VERSION_MAPPING.get(version, None)
        if info_class is None:
            raise ValueError(f"No matching library info version for {version}")
        self.info = info_class(self.lib_file_path, **kwargs)

    def __str__(self) -> str:
        return f'Library["{self.lib_file_path}", {self.info}]'

    __repr__ = __str__

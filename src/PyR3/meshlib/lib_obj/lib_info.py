# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pathlib import Path

from packaging.version import Version

from .model_info import ModelInfoV1_0_0


class LibraryInfoBase:
    pass


@dataclass
class LibraryInfoV1_0_0(LibraryInfoBase):
    lib_file_path: Path
    name: str
    author: str
    description: str
    lib_version: Version
    model_list: list

    def __post_init__(self) -> None:
        self.lib_file_path = Path(self.lib_file_path)
        self.lib_version = Version(self.lib_version)
        model_list = []
        for model_info in self.model_list:
            model_list.append(
                ModelInfoV1_0_0(
                    self.lib_file_path.parent,
                    **model_info,
                )
            )
        self.model_list = model_list

    def __str__(self) -> str:
        return f"{self.name} {self.lib_version} by {self.author}"

    def dict(self) -> str:
        return {
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "lib_version": self.lib_version.public,
            "model_list": [model.dict() for model in self.model_list],
        }

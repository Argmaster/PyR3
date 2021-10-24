# -*- coding: utf-8 -*-
from pathlib import Path

from .model_info import ModelInfoV1_0_0


class LibraryInfoBase:
    pass


class LibraryInfoV1_0_0(LibraryInfoBase):
    path: str
    name: str
    author: str
    description: str
    lib_version: str
    model_list: list

    def __init__(
        self,
        path: str,
        name: str,
        author: str,
        description: str,
        lib_version: str,
        model_list: list,
    ) -> None:
        self.path = Path(path)
        self.name = name
        self.author = author
        self.description = description
        self.lib_version = lib_version
        self.model_list = []
        for model_info in model_list:
            self.model_list.append(
                ModelInfoV1_0_0(
                    self.path.parent,
                    **model_info,
                )
            )

    def __str__(self) -> str:
        return f"{self.name} {self.lib_version} by {self.author}"

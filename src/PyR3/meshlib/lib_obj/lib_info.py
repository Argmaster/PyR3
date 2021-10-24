# -*- coding: utf-8 -*-
from .model_info import ModelInfo


class LibraryInfoBase:
    pass


class LibraryInfoV1_0_0(LibraryInfoBase):
    name: str
    author: str
    description: str
    lib_version: str
    model_list: list

    def __init__(
        self,
        name: str,
        author: str,
        description: str,
        lib_version: str,
        model_list: list,
    ) -> None:
        self.name = name
        self.author = author
        self.description = description
        self.lib_version = lib_version
        self.model_list = []
        for model_info in model_list:
            self.model_list.append(ModelInfo())

    def __str__(self) -> str:
        return f"{self.name} {self.lib_version} by {self.author}"

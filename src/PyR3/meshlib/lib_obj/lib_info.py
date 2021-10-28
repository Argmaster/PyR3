# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional

from packaging.version import Version
from pydantic import BaseModel, validator

from .model_info import ModelInfoV1_0_0


class LibraryInfoBase(BaseModel):
    pass


class LibraryInfoV1_0_0(LibraryInfoBase):
    lib_file_path: Path
    name: str
    author: str
    description: str
    lib_version: Version
    model_list: List

    class Config:
        arbitrary_types_allowed = True

    @validator("lib_file_path", pre=True)
    def _lib_file_path_to_Path_type(cls, path: str):
        return Path(path)

    @validator("lib_version", pre=True)
    def _lib_version_to_Version(cls, version: str):
        return Version(version)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._convert_models_into_classes()

    def _convert_models_into_classes(self) -> None:
        model_list = []
        directory = self.lib_file_path.parent
        for model_info in self.model_list:
            mi = ModelInfoV1_0_0(
                directory=directory,
                **model_info,
            )
            if mi not in model_list:
                model_list.append(mi)
        self.model_list = model_list

    def match_hash(self, hash_: str) -> Optional[ModelInfoV1_0_0]:
        for model in self.model_list:
            if model.match_hash(hash_):
                return model
        raise KeyError(f"Model with hash '{hash_}' not found.")

    def match_tag(self, tag: str) -> List[ModelInfoV1_0_0]:
        return [model for model in self.model_list if model.match_tag(tag)]

    def dict(self, *_, **__) -> dict:
        return {
            "version": "1.0.0",
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "lib_version": self.lib_version.public,
            "model_list": [model.dict() for model in self.model_list],
        }

    def __eq__(self, other: LibraryInfoV1_0_0) -> bool:
        return isinstance(other, LibraryInfoV1_0_0) and (
            self.name == other.name
            and self.author == other.author
            and self.description == other.description
            and self.lib_version == other.lib_version
            and self.model_list == other.model_list
        )

    def __str__(self) -> str:
        return f"{self.name} {self.lib_version} by {self.author}"

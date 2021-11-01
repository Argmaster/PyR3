# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import List

from packaging.version import Version
from pydantic import BaseModel, validator

from .model_info import ModelInfoV1_0_0


class LibraryInfoV1_0_0(BaseModel):
    lib_file_path: Path
    name: str
    author: str
    description: str
    lib_version: Version
    model_list: List[ModelInfoV1_0_0]

    class Config:
        arbitrary_types_allowed = True

    @validator("lib_file_path", pre=True)
    def _lib_file_path_to_Path_type(cls, path: str):
        return Path(path)

    @validator("lib_version", pre=True)
    def _lib_version_to_Version(cls, version: str):
        return Version(version)

    @validator("model_list", pre=True)
    def _convert_models_into_classes(cls, value, values):
        model_list = []
        directory = Path(values.get("lib_file_path")).parent
        for model_info in value:
            mi = ModelInfoV1_0_0(
                directory=directory,
                **model_info,
            )
            if mi not in model_list:
                model_list.append(mi)
        return model_list

    def match_hash(self, hash_: str) -> ModelInfoV1_0_0:
        """Finds first ModelInfo object with matching hash contained in this
        library. If no model with matching hash is found, KeyError is raised.

        :param hash_: Hash to look for.
        :type hash_: str
        :raises KeyError: Raised if no model is found.
        :return: Matching ModelInfo object.
        :rtype: ModelInfoV1_0_0
        """
        for model in self.model_list:
            if model.match_hash(hash_):
                return model
        raise KeyError(f"Model with hash '{hash_}' not found.")

    def match_tag(self, tag: str) -> List[ModelInfoV1_0_0]:
        """Find all ModelInfo objects in this libraries that have tag in their
        tag list.

        :param tag: Tag to look for.
        :type tag: str
        :return: List containing all matching models. If none is found, empty list is returned.
        :rtype: List[ModelInfoV1_0_0]
        """
        return [model for model in self.model_list if model.match_tag(tag)]

    def dict(self, *_, **__) -> dict:
        """Generate dictionary representation of a object.

        :return: dictionary containing json-serializable contents of this class.
        :rtype: dict
        """
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

# -*- coding: utf-8 -*-
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

    def match_hash(self, _hash: str) -> Optional[ModelInfoV1_0_0]:
        """Searches models contained in this library to find model
        with matching hash. If model is found, it is instantly returned,
        if no model is found, ValueError is being raised.

        :param _hash: hash value to look for.
        :type _hash: str
        :raises ValueError: raised if no matching model found.
        :return: model if found.
        :rtype: Optional[ModelInfoV1_0_0]
        """
        for model in self.model_list:
            if model.match_hash(_hash):
                return model
        raise ValueError(f"Model with hash '{_hash}' not found.")

    def match_tag(self, tag: str) -> List[ModelInfoV1_0_0]:
        """Searches models contained in this library to find models
        with matching tags. Models found are appended to list, which
        is later returned. If no models is found, empty list is returned.

        :param tag: tag value to look for.
        :type tag: str
        :return: list of models found.
        :rtype: List[ModelInfoV1_0_0]
        """
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

    def __str__(self) -> str:
        return f"{self.name} {self.lib_version} by {self.author}"

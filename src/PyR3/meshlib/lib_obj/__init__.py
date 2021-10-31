# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml

from .lib_info import LibraryInfoBase, LibraryInfoV1_0_0
from .model_info import ModelInfoBase, ModelInfoV1_0_0
from .usertags import load as load_usertags


def load(lib_file_path: str) -> LibraryObject:
    with open(lib_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return LibraryObject(Path(lib_file_path), **data)


def dump(
    ob: LibraryObject | LibraryInfoBase | ModelInfoBase, lib_file_path: str
):
    with open(lib_file_path, "w", encoding="utf-8") as file:
        yaml.dump(
            ob.dict(), file, indent=2, allow_unicode=True, sort_keys=False
        )


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
        self.user_tags = load_usertags(
            self.lib_file_path.parent / "__user__.yaml"
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

    def match_hash(self, hash_: str) -> Optional[ModelInfoV1_0_0]:
        """Searches models contained in this library to find model
        with matching hash. If model is found, it is instantly returned,
        if no model is found, ValueError is being raised.

        :param hash_: hash value to look for.
        :type hash_: str
        :raises ValueError: raised if no matching model found.
        :return: model if found.
        :rtype: Optional[ModelInfoV1_0_0]
        """
        return self.info.match_hash(hash_)

    def match_tag(self, tag: str) -> List[ModelInfoV1_0_0]:
        """Searches models contained in this library to find models
        with matching tags. Models found are appended to list, which
        is later returned. If no models is found, empty list is returned.

        :param tag: tag value to look for.
        :type tag: str
        :return: list of models found.
        :rtype: List[ModelInfoV1_0_0]
        """
        matching_models = self.info.match_tag(tag)
        extra_hashes = self.user_tags.get_hash_with_tag(tag)
        for extra_hash in extra_hashes:
            extra_model = self.match_hash(extra_hash)
            if extra_model not in matching_models:
                matching_models.append(extra_model)
        return matching_models

    def __eq__(self, o: LibraryObject) -> bool:
        return isinstance(o, LibraryObject) and self.info == o.info

    def __str__(self) -> str:
        return f'Library[{self.info} at "{self.lib_file_path}"]'

    __repr__ = __str__

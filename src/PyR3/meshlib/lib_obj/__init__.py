# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import zipfile
from pathlib import Path
from typing import ClassVar, List, Optional, Set

import yaml

from .lib_info import LibraryInfoV1_0_0
from .model_info import ModelInfoV1_0_0
from .usertags import load as load_usertags


def load(lib_file_path: str) -> LibraryObject:
    with open(lib_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return LibraryObject(Path(lib_file_path), **data)


def dump(
    ob: LibraryObject | LibraryInfoV1_0_0 | ModelInfoV1_0_0, lib_file_path: str
):
    with open(lib_file_path, "w", encoding="utf-8") as file:
        yaml.dump(
            ob.dict(), file, indent=2, allow_unicode=True, sort_keys=False
        )


class LibraryObject:

    COMPRESSION: ClassVar[int] = zipfile.ZIP_LZMA
    ARCHIVE_EXTENSION: ClassVar[str] = "ms.lib"
    INFO_VERSION_MAPPING = {"1.0.0": LibraryInfoV1_0_0}
    lib_file_path: Path
    info: LibraryInfoV1_0_0

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

    def pack(self, directory: str | Path = ".", file_name: str | Path = None):
        if file_name is None:
            file_name = f"{self.info.name}.{self.ARCHIVE_EXTENSION}"
        file_path = Path(directory) / Path(file_name)
        with zipfile.ZipFile(
            file_path,
            "w",
            compression=self.COMPRESSION,
        ) as archive:
            self._pack_lib_contents_into_archive(archive)

    def _pack_lib_contents_into_archive(self, archive):
        lib_file_path = self.info.lib_file_path
        archive.write(lib_file_path, arcname=lib_file_path.name)
        lib_dir = lib_file_path.parent.resolve()
        for model in self.info.model_list:
            model_path = model.import_path
            archive.write(model_path, arcname=model_path.relative_to(lib_dir))

    def unpack(self, file_path: Path, target_dir: str | Path = None):
        file_name = os.path.basename(file_path).split(".")[0]
        with zipfile.ZipFile(file_path, "r") as archive:
            archive.extractall(path=target_dir / file_name)

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
        """Searches models contained in this library to find model with
        matching hash. If model is found, it is instantly returned, if no model
        is found, ValueError is being raised.

        :param hash_: hash value to look for.
        :type hash_: str
        :raises ValueError: raised if no matching model found.
        :return: model if found.
        :rtype: Optional[ModelInfoV1_0_0]
        """
        return self.info.match_hash(hash_)

    def match_tag(self, tag: str) -> List[ModelInfoV1_0_0]:
        """Searches models contained in this library to find models with
        matching tags. Models found are appended to list, which is later
        returned. If no models is found, empty list is returned.

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

    def get_all_tags_associated_with_model(
        self, mi: ModelInfoV1_0_0
    ) -> Set[str]:
        """Fetches all tags associated with model and returns it as a set.

        :param mi: Model to fetch tags for.
        :type mi: ModelInfoV1_0_0
        :return: Set of all tags.
        :rtype: Set[str]
        """
        all_tags = []
        all_tags.extend(mi.tags.copy())
        all_tags.extend(self.user_tags.get_extra_tags(mi.hash))
        return set(all_tags)

    def __eq__(self, o: LibraryObject) -> bool:
        return isinstance(o, LibraryObject) and self.info == o.info

    def __str__(self) -> str:
        return f'Library[{self.info} at "{self.lib_file_path}"]'

    __repr__ = __str__

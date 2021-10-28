# -*- coding: utf-8 -*-
from glob import glob
from pathlib import Path
from typing import Iterable, List

from .lib_obj import LibraryObject, load


class LibraryManager:

    PATH: List[Path]
    LIBS: List[LibraryObject]

    def __init__(self, lib_path: List[str]) -> None:
        self.set_path(lib_path)

    def set_path(self, lib_path: List[str]):
        self.PATH = [Path(path).resolve() for path in lib_path]
        self._find_libs()

    def _find_libs(self):
        self.LIBS = []
        for sub_path in self.PATH:
            self.LIBS.extend(self._find_lib_files(sub_path))

    def _find_lib_files(self, dir_path: Path) -> Iterable[LibraryObject]:
        libraries = []
        for glob_pattern in (
            str(dir_path / "__lib__.yaml"),
            str(dir_path / "*" / "__lib__.yaml"),
        ):
            for file_path in glob(glob_pattern):
                library_object = load(file_path)
                if library_object not in libraries:
                    libraries.append(library_object)
        return libraries

    def get_by_hash(self, hash_: str):
        """Searches models contained in all libraries to find model
        with matching hash. If model is found, it is instantly returned,
        if no model is found, ValueError is being raised.

        :param hash_: hash value to look for.
        :type hash_: str
        :raises ValueError: raised if no matching model found.
        :return: model if found.
        :rtype: Optional[ModelInfoV1_0_0]
        """
        for library in self.LIBS:
            try:
                return library.match_hash(hash_)
            except KeyError:
                pass
        raise KeyError(f"Model with hash '{hash_}' not found.")

    def get_by_tag(self, tag: str):
        """Searches models contained in all libraries to find models
        with matching tag. Models found are appended to list, which
        is later returned. If no models is found, empty list is returned.

        :param tag: tag value to look for.
        :type tag: str
        :return: list of models found.
        :rtype: List[ModelInfoV1_0_0]
        """
        models = []
        for library in self.LIBS:
            models.extend(library.match_tag(tag))
        return models

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

    def get_by_hash(self, hash: str):
        pass

    def get_by_tag(self, tag: str):
        pass

    def get_by_author_tag(self, tag: str):
        pass

    def get_by_user_tag(self, tag: str):
        pass

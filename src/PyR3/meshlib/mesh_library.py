# -*- coding: utf-8 -*-


from pathlib import Path
from typing import List


class MeshLibrary:

    path: List[Path]

    def __init__(self, lib_path: List[str] = ["meshlib"]) -> None:
        self.path = []
        self.extend_path(lib_path)

    def extend_path(self, lib_path: List[str]):
        lib_path = [Path(path).resolve() for path in lib_path]
        self.path.extend(lib_path)
        self._find_libs()

    def _find_libs(self):
        for path in self.path:
            self._find_lib_files(path)

    def _find_lib_files(self, path: Path):
        pass

    def get_by_hash(self, hash: str):
        pass

    def get_by_tag(self, tag: str):
        pass

    def get_by_author_tag(self, tag: str):
        pass

    def get_by_user_tag(self, tag: str):
        pass

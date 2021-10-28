# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib import LibraryManager

DIR = Path(__file__).parent


class TestMeshLibrary(TestCase):
    def test_MeshLibrary_instantiate_with_paths(self):
        paths = ["."]
        lib = LibraryManager(paths)
        self.assertTrue(isinstance(lib.PATH[0], Path))
        self.assertTrue(lib.PATH[0] == Path(paths[0]).resolve())

    def test_MeshLibrary_find_library(self):
        lib = LibraryManager([DIR / "test_lib"])
        self.assertTrue(len(lib.LIBS) == 1)


if __name__ == "__main__":
    main()

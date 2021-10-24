# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib.mesh_library import LibraryManager


class TestMeshLibrary(TestCase):
    def test_MeshLibrary_instantiate_with_paths(self):
        paths = ["."]
        lib = LibraryManager(paths)
        self.assertTrue(isinstance(lib.PATH[0], Path))
        self.assertTrue(lib.PATH[0] == Path(paths[0]).resolve())

    def test_MeshLibrary_find_library(self):
        lib = LibraryManager([Path(__file__).parent / "test_lib"])
        print(lib.LIBS)


if __name__ == "__main__":
    main()

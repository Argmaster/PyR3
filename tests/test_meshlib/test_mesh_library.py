# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib.mesh_library import MeshLibrary


class TestMeshLibrary(TestCase):
    def test_MeshLibrary_instantiate_with_paths(self):
        paths = ["."]
        lib = MeshLibrary(paths)
        self.assertTrue(isinstance(lib.path[0], Path))
        self.assertTrue(lib.path[0] == Path(paths[0]).resolve())


if __name__ == "__main__":
    main()

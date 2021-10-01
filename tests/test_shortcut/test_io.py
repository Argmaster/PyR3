# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from unittest import TestCase, main

from PyR3.shortcut.context import Objects, wipeScenes
from PyR3.shortcut.io import export_to, import_from
from PyR3.shortcut.mesh import addCube


TESTS_TEMP = Path(__file__).parent.parent / ".temp"
TESTS_TEMP.mkdir(parents=True, exist_ok=True)


class TestIO(TestCase):

    def test_export_global(self):
        wipeScenes()
        addCube()
        addCube(location=(1, 1, 1))
        export_to(TESTS_TEMP / "test_export_global.glb")

    def test_export_selected(self):
        wipeScenes()
        addCube()
        addCube(location=(-1, -1, -1))
        export_to(TESTS_TEMP / "test_export_global.blend")

    def test_import_selected(self):
        wipeScenes()
        addCube()
        addCube(location=(-1, -1, -1))
        export_to(TESTS_TEMP / "test_export_global.blend")
        wipeScenes()
        import_from(TESTS_TEMP / "test_export_global.blend")
        self.assertEqual(len(Objects.all()), 2)


if __name__ == "__main__":
    main()

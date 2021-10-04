# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase
from unittest import main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to
from PyR3.shortcut.mesh import addCube
from PyR3.shortcut.mesh import addPlane
from PyR3.shortcut.mesh import join
from PyR3.shortcut.modifiers import Array
from PyR3.shortcut.modifiers import Bevel
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.modifiers import Decimate
from PyR3.shortcut.modifiers import Solidify

TEMP_FOLDER = Path(__file__).parent / ".temp"
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)


class TestModifiers(TestCase):
    def prepare_Boolean(self):
        wipeScenes()
        o1 = addCube()
        o2 = addCube(location=(1, 1, 1))
        return o1, o2

    def test_Boolean_difference(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2, operation="DIFFERENCE").apply()
        export_to(filepath=TEMP_FOLDER / "test_Boolean_difference.blend")

    def test_Boolean_union(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2, operation="UNION").apply()
        export_to(filepath=TEMP_FOLDER / "test_Boolean_union.blend")

    def test_Boolean_intersect(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2).apply(operation="INTERSECT")
        export_to(filepath=TEMP_FOLDER / "test_Boolean_intersect.blend")

    def test_Array(self):
        wipeScenes()
        o = addCube()
        Array(o, (0, 0, 2), count=3).apply()
        export_to(filepath=TEMP_FOLDER / "test_Array.blend")

    def test_Solidify(self):
        wipeScenes()
        o = addPlane()
        Solidify(o, 0.4, 1).apply()
        export_to(filepath=TEMP_FOLDER / "test_Solidify.blend")

    def test_Bevel(self):
        wipeScenes()
        o = addCube()
        Bevel(o, width=0.2).apply()
        export_to(filepath=TEMP_FOLDER / "test_Bevel.blend")

    def test_Decimate(self):
        wipeScenes()
        o = addCube()
        o1 = addCube(location=(1, 1, 0))
        join(o, o1)
        Decimate(o, decimate_type="DISSOLVE").apply()
        export_to(filepath=TEMP_FOLDER / "test_Decimate.blend")


if __name__ == "__main__":
    main()

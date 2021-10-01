# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.modifiers import Bevel, Boolean, Array, Solidify
from PyR3.shortcut.mesh import addCube, addPlane
from PyR3.shortcut.io import export_blend


class TestModifiers(TestCase):
    def prepare_Boolean(self):
        wipeScenes()
        o1 = addCube()
        o2 = addCube(location=(1, 1, 1))
        return o1, o2

    def test_Boolean_difference(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2, operation="DIFFERENCE").apply()
        export_blend(filepath="./tests/.temp/test_Boolean_difference.blend")

    def test_Boolean_union(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2, operation="UNION").apply()
        export_blend(filepath="./tests/.temp/test_Boolean_union.blend")

    def test_Boolean_intersect(self):
        o1, o2 = self.prepare_Boolean()
        Boolean(o1, o2).apply(operation="INTERSECT")
        export_blend(filepath="./tests/.temp/test_Boolean_intersect.blend")

    def test_Array(self):
        wipeScenes()
        o = addCube()
        Array(o, (0, 0, 2), count=3).apply()
        export_blend(filepath="./tests/.temp/test_Array.blend")

    def test_Solidify(self):
        wipeScenes()
        o = addPlane()
        Solidify(o, 0.4, 1).apply()
        export_blend(filepath="./tests/.temp/test_Solidify.blend")

    def test_Bevel(self):
        wipeScenes()
        o = addCube()
        Bevel(o, width=0.2).apply()
        export_blend(filepath="./tests/.temp/test_Bevel.blend")


if __name__ == "__main__":
    main()

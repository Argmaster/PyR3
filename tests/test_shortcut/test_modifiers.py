# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.mesh import addCube
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
        Boolean(o1, o2, operation="INTERSECT").apply()
        export_blend(filepath="./tests/.temp/test_Boolean_intersect.blend")


if __name__ == "__main__":
    main()

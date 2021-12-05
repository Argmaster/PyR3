# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase

from PyR3.shortcut.context import Objects, wipeScenes
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.io import export_to
from PyR3.shortcut.mesh import addCube, fromPyData, join
from PyR3.shortcut.transform import Transform


class TestMeshModule(TestCase):
    def test_fromPyData(self):
        wipeScenes()
        obj = fromPyData(
            [(0, 0, 0), (0, 1, 1), (0, 3, 0)],
            [(0, 1), (1, 2), (2, 0)],
            [(0, 1, 2)],
        )
        with Edit(obj) as edit:
            self.assertEqual(len(edit.vertices()), 3)
            self.assertEqual(len(edit.edges()), 3)
            self.assertEqual(len(edit.faces()), 1)
        Transform.rotate(0.66, "Z").apply_all()
        export_to(filepath="./tests/.temp/fromPyData.blend")

    def test_join(self):
        wipeScenes()
        o1 = addCube()
        o2 = addCube()
        join(o1, o2)
        self.assertEqual(len(Objects.all()), 1)

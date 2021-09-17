# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main

import bpy


from PyR3.shortcut.context import Objects, cleanScene
from PyR3.shortcut.mesh import addCube

class Test(TestCase):

    def test_get_active(self):
        cleanScene()
        active = addCube()
        self.assertEqual(Objects.active, active)

    def test_set_active(self):
        cleanScene()
        old = addCube()
        new = addCube()
        Objects.active = old
        self.assertEqual(Objects.active, old)
        self.assertNotEqual(Objects.active, new)

    def test_selected(self):
        cleanScene()
        old = addCube()
        new = addCube()
        self.assertEqual([new], Objects.selected)
        self.assertNotEqual([old], Objects.selected)

    def test_select(self):
        cleanScene()
        old = addCube()
        new = addCube()
        Objects.select(old)
        self.assertEqual([old, new], Objects.selected)

    def test_deselect(self):
        cleanScene()
        old = addCube()
        new = addCube()
        Objects.deselect(new)
        self.assertEqual([], Objects.selected)

    def prepare_3_elem_scene(self):
        cleanScene()
        older = addCube()
        old = addCube()
        new = addCube()
        Objects.select_all()
        return older, old, new

    def test_select_all(self):
        older, old, new = self.prepare_3_elem_scene()
        self.assertEqual([older, old, new], Objects.selected)

    def test_deselect_all(self):
        self.prepare_3_elem_scene()
        Objects.deselect_all()
        self.assertEqual([], Objects.selected)

    def test_select_only(self):
        older, *_ = self.prepare_3_elem_scene()
        Objects.select_only(older)
        self.assertEqual([older], Objects.selected)

    def test_delete(self):
        older, *rest = self.prepare_3_elem_scene()
        Objects.delete(older)
        self.assertEqual(list(rest), Objects.selected)

    def test_delete_all(self):
        self.prepare_3_elem_scene()
        Objects.delete_all()
        Objects.select_all()
        self.assertEqual([], Objects.selected)

    def test_duplicate(self):
        objects = self.prepare_3_elem_scene()
        Objects.duplicate(*objects)
        Objects.select_all()
        self.assertEqual(len(Objects.selected), 6)

    def test_inverse_selection(self):
        older, *rest = self.prepare_3_elem_scene()
        Objects.select_only(older)
        Objects.inverse_selection()
        self.assertEqual(rest, Objects.selected)


if __name__ == '__main__':
    main()
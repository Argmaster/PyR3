# -*- coding: utf-8 -*-
from __future__ import annotations
from re import L
from unittest import TestCase, main

import bpy


from PyR3.shortcut.context import (
    Objects,
    cleanScene,
    wipeScenes,
    delScene,
    getScene,
    listScenes,
    newScene,
    setScene,
    temporarily_selected,
)
from PyR3.shortcut.mesh import addCube


class TestObjectsOps(TestCase):
    def test_get_active(self):
        wipeScenes()
        active = addCube()
        self.assertEqual(Objects.active, active)

    def test_set_active(self):
        wipeScenes()
        old = addCube()
        new = addCube()
        Objects.active = old
        self.assertEqual(Objects.active, old)
        self.assertNotEqual(Objects.active, new)

    def test_selected(self):
        wipeScenes()
        old = addCube()
        new = addCube()
        self.assertEqual([new], Objects.selected)
        self.assertNotEqual([old], Objects.selected)

    def test_select(self):
        wipeScenes()
        old = addCube()
        new = addCube()
        Objects.select(old)
        self.assertEqual([old, new], Objects.selected)

    def test_deselect(self):
        wipeScenes()
        old = addCube()
        new = addCube()
        Objects.deselect(new)
        self.assertEqual([], Objects.selected)

    def prepare_3_elem_scene(self):
        wipeScenes()
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
        self.assertEqual(rest, Objects.selected)

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

    def test_select_contained(self):
        objects = self.prepare_3_elem_scene()
        Objects.deselect_all()
        Objects(objects).select_contained()
        self.assertEqual(len(Objects.selected), 3)

    def test_deselect_contained(self):
        objects = self.prepare_3_elem_scene()
        Objects(objects).deselect_contained()
        self.assertEqual(len(Objects.selected), 0)

    def test_select_only_contained(self):
        omitted, *rest = self.prepare_3_elem_scene()
        Objects(rest).select_only_contained()
        self.assertEqual(rest, Objects.selected)

    def test_get_only(self):
        ob, *_ = self.prepare_3_elem_scene()
        self.assertRaises(ValueError, lambda: Objects.selected.only())
        Objects.select_only(ob)
        self.assertEqual(ob, Objects.selected.only())

    def test_str(self):
        wipeScenes()
        ob = addCube()
        self.assertEqual(
            str(Objects.selected), f"Objects[bpy.data.objects['{ob.name}']]"
        )

    def test_temporarily_selected(self):
        wipeScenes()
        ob = addCube()
        ob_2 = addCube()
        self.assertEqual(Objects.selected, [ob_2])
        with temporarily_selected(ob):
            self.assertEqual(Objects.selected, [ob])
        self.assertEqual(Objects.selected, [ob_2])


class TestSceneOps(TestCase):
    def test_getScene(self):
        wipeScenes()
        self.assertTrue(isinstance(getScene(), bpy.types.Scene))

    def test_listScenes(self):
        wipeScenes()
        self.assertEqual(len(listScenes()), 1)

    def test_newScene(self):
        wipeScenes()
        old_scene = getScene()
        newScene()
        self.assertEqual(len(listScenes()), 2)
        self.assertNotEqual(getScene(), old_scene)

    def test_setScene(self):
        wipeScenes()
        old_scene = getScene()
        newScene()
        setScene(old_scene)
        self.assertEqual(old_scene, getScene())
        self.assertEqual(len(listScenes()), 2)

    def test_delScene(self):
        wipeScenes()
        old_scene = getScene()
        newScene()
        self.assertEqual(len(listScenes()), 2)
        delScene()
        self.assertEqual(getScene(), old_scene)
        self.assertEqual(len(listScenes()), 1)

    def test_wipeScenes(self):
        newScene()
        self.assertNotEqual(len(listScenes()), 1)
        wipeScenes()
        self.assertEqual(len(listScenes()), 1)

    def test_cleanScene(self):
        wipeScenes()
        cube: bpy.types.Object = addCube()
        self.assertTrue(len(getScene().objects) == 1)
        cleanScene()
        self.assertTrue(len(getScene().objects) == 0)


if __name__ == "__main__":
    main()

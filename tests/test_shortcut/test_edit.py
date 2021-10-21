# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import addCube


class Test(TestCase):
    def test_with_statement(self):
        wipeScenes()
        ob = addCube()
        self.assertFalse(Edit.isEditMode())
        with Edit(ob):
            self.assertTrue(Edit.isEditMode())
        self.assertFalse(Edit.isEditMode())

    def test_vertices(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            self.assertEqual(len(mesh.vertices()), 8)

    def test_edges(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            self.assertEqual(len(mesh.edges()), 12)

    def test_faces(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            self.assertEqual(len(mesh.faces()), 6)

    def test_select_deselect(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            # selected
            mesh.select_all()
            count = 0
            for v in mesh.vertices():
                count += 1
                self.assertTrue(v.select)
            self.assertEqual(count, 8)
            # deselected
            mesh.deselect_all()
            count = 0
            for v in mesh.vertices():
                count += 1
                self.assertFalse(v.select)
            self.assertEqual(count, 8)

    def test_select_above(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.select_vertices(lambda co: co.z > 0.5)
            for v in mesh.vertices():
                if v.co.z > 0:
                    self.assertTrue(v.select)
                else:
                    self.assertFalse(v.select)

    def test_selection_invert(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.invert_selection()
            self.assertEqual(len(mesh.get_selected_vertices()), 8)

    def test_delete_vertices(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.select_vertices(lambda co: co.z > 0.5)
            mesh.delete_vertices()
            self.assertEqual(len(mesh.vertices()), 4)

    def test_delete_edges(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.select_edges(lambda p1, p2: (p1.z > 0.5 and p2.z > 0.5))
            mesh.delete_edges()
            self.assertEqual(len(mesh.edges()), 8)

    def test_delete_faces(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.select_facing((0, 0, 1))
            mesh.delete_faces()
            self.assertEqual(len(mesh.faces()), 5)

    def test_duplicate(self):
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.deselect_all()
            mesh.vertices()[0].select_set(True)
            mesh.duplicate()
            self.assertEqual(len(mesh.vertices()), 9)

    def test_bevel(self):
        """This one tests wheather it is possible to call
        functions from blender API assigned to attributes
        of Edit class. Therefore it applies for all this style
        functions.
        """
        wipeScenes()
        ob = addCube()
        with Edit(ob) as mesh:
            mesh.bevel(offset=0.1)
            self.assertEqual(len(mesh.vertices()), 24)


if __name__ == "__main__":
    main()

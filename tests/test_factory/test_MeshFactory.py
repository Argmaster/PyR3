# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory, getfields
from PyR3.shortcut.context import Objects, cleanScene
from PyR3.shortcut.mesh import addCylinder, addCube


class TestMeshFactory(TestCase):
    class Subclass(MeshFactory):

        """subclass"""

        __author__ = "Krzysztof Wiśniewski"
        __version__ = [1, 0, 0]

        field1 = Length
        field2 = Length

        def render(self, test: TestCase):
            test.assertEqual(len(Objects.selected), 0)
            addCylinder()
            test.assertEqual(len(Objects.selected), 1)

    class Subclass2(Subclass):

        """subclass"""

        __author__ = "Krzysztof Wiśniewski"
        __version__ = [1, 0, 0]

        field3 = Length

        def render(self, test: TestCase):
            test.assertEqual(len(Objects.selected), 0)
            addCylinder()
            test.assertEqual(len(Objects.selected), 1)
            Objects.deselectAll()

    def test_get_fields(self):
        self.assertEqual(getfields(self.Subclass), self.Subclass.__dict__["$fields"])
        self.assertEqual(
            getfields(
                self.Subclass(
                    {
                        "field1": "3mm",
                        "field2": "2mm",
                    }
                )
            ),
            self.Subclass.__dict__["$fields"],
        )

    def test_subclassing(self):
        self.assertTrue("field1" in getfields(self.Subclass))
        self.assertTrue("field2" in getfields(self.Subclass))

        self.assertTrue("field1" in getfields(self.Subclass2))
        self.assertTrue("field2" in getfields(self.Subclass2))
        self.assertTrue("field3" in getfields(self.Subclass2))

    def test_required_members(self):
        self.assertRaises(TypeError, self._class_with_missing_members)

    def _class_with_missing_members(self):
        class Subclass(MeshFactory):

            """subclass"""

            def render(self):
                pass

    def clean_workspace(self):
        cleanScene()
        addCube()
        Objects.selectAll()

    def test_render_with_return(self):
        self.clean_workspace()
        self.assertEqual(len(Objects.selected), 1)
        self.Subclass(
            {
                "field1": "3mm",
                "field2": "2mm",
            }
        ).render(self)
        Objects.selectAll()
        self.assertEqual(len(Objects.selected), 2)

    def test_render_without_return(self):
        self.clean_workspace()
        self.assertEqual(len(Objects.selected), 1)
        self.Subclass2(
            {
                "field1": "3mm",
                "field2": "2mm",
                "field3": "2mm",
            }
        ).render(self)
        Objects.selectAll()
        self.assertEqual(len(Objects.selected), 1)

    def test_render_select_space(self):
        self.clean_workspace()

        class TestMeshFactory(MeshFactory):

            """subclass"""

            __author__ = "Krzysztof Wiśniewski"
            __version__ = [1, 0, 0]

            def render(self, test: TestCase):
                Objects.selectAll()
                test.assertEqual(len(Objects.selected), 0)
                addCylinder()
                Objects.selectAll()
                test.assertEqual(len(Objects.selected), 1)

        addCylinder()
        addCylinder()
        TestMeshFactory({}).render(self)
        Objects.selectAll()
        self.assertEqual(len(Objects.selected), 4)


if __name__ == "__main__":
    main()

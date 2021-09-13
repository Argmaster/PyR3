# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory, getfields


class TestMeshFactory(TestCase):


    class Subclass(MeshFactory):

        """subclass"""

        __author__ = "Krzysztof Wiśniewski"
        __version__ = [1, 0, 0]

        field1 = Length
        field2 = Length

        def render(self):
            pass

    class Subclass2(Subclass):

        """subclass"""

        __author__ = "Krzysztof Wiśniewski"
        __version__ = [1, 0, 0]

        field3 = Length

    def test_get_fields(self):
        self.assertEqual(getfields(self.Subclass), self.Subclass.__dict__['$fields'])
        self.assertEqual(getfields(self.Subclass({
            "field1": "3mm",
            "field2": "2mm",
        })), self.Subclass.__dict__['$fields'])

    def test_subclassing(self):
        self.assertTrue("field1" in getfields(self.Subclass))
        self.assertTrue("field2" in getfields(self.Subclass))

        self.assertTrue("field1" in getfields(self.Subclass2))
        self.assertTrue("field2" in getfields(self.Subclass2))
        self.assertTrue("field3" in getfields(self.Subclass2))

    def test_required_membders(self):
        self.assertRaises(TypeError, self._class_with_missing_members)

    def _class_with_missing_members(self):

        class Subclass(MeshFactory):

            """subclass"""


            def render(self):
                pass



if __name__ == '__main__':
    main()

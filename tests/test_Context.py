# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main
from PyR3.shortcut.context import Objects


from bpy.ops import mesh

class TestContext(TestCase):

    def test_selection(self):
        cube = Objects.selected.only()
        print(cube)
        mesh.primitive_cone_add()
        cone = Objects.selected.only()
        print(cone)





if __name__ == '__main__':
    main()
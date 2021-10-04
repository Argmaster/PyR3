# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase
from unittest import main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to
from PyR3.shortcut.material import new_node_material
from PyR3.shortcut.material import set_material
from PyR3.shortcut.material import update_BSDF_node
from PyR3.shortcut.mesh import addCube

TESTS_TEMP = Path(__file__).parent.parent / ".temp"

TESTS_TEMP.mkdir(parents=True, exist_ok=True)


class TestMaterial(TestCase):
    def test_new_material_and_assign(self):
        wipeScenes()
        ob = addCube()
        material = new_node_material()
        update_BSDF_node(material, color=(0.5, 0.5, 0.0, 1.0))
        set_material(ob, material)
        export_to(TESTS_TEMP / "test_new_material_and_assign.blend")


if __name__ == "__main__":
    main()

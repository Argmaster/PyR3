# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to
from PyR3.shortcut.material import new_node_material, set_material, update_BSDF_node
from PyR3.shortcut.mesh import addCube

TESTS_TEMP = Path(__file__).parent.parent / ".temp"

TESTS_TEMP.mkdir(parents=True, exist_ok=True)


class TestMaterial(TestCase):
    def test_new_material_update_all(self):
        wipeScenes()
        ob = addCube()
        material = new_node_material()
        update_BSDF_node(
            material,
            color=(0.5, 0.5, 0.0, 1.0),
            subsurface=0.4,
            subsurfaceRadius=(0.0, 0.0, 0.0),
            subsurfaceColor=(0.0, 0.44, 0.44, 1.0),
            metallic=0.33,
            roughness=0.33,
            specular=0.1,
            specularTint=0.2,
            anisotropic=0.1,
            anisotropicRotation=0.1,
            sheen=0.1,
            sheenTint=0.1,
            clearcoat=0.33,
            clearcoatRoughness=0.2,
            emission=(0.1, 0.1, 0.5, 0.5),
            emissionStrength=0.66,
            alpha=0.5,
        )
        set_material(ob, material)
        export_to(TESTS_TEMP / "test_new_material_and_assign.blend")

    def test_new_material_update_none(self):
        wipeScenes()
        ob = addCube()
        material = new_node_material()
        update_BSDF_node(material)
        set_material(ob, material)
        export_to(TESTS_TEMP / "test_new_material_and_assign.blend")

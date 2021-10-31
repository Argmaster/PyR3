# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.construct.mp import MeshProject

DIR = Path(__file__).parent
TEST_MP_FP = DIR / "test.mp.yaml"
MP_TEST_COMP_1 = {
    "symbol": "A1",
    "hash": "",
    "tags": [],
    "x": 0.0,
    "y": 0.0,
    "rotation": 90.0,
    "is_top": True,
}
MP_TEST_CONTENT = {
    "project_file_path": TEST_MP_FP,
    "project_name": "Test Project",
    "description": "",
    "scale": 100,
    "component_list": [MP_TEST_COMP_1],
}


class TestMeshProject(TestCase):
    def test_dump_load(self):
        mp = MeshProject(**MP_TEST_CONTENT)
        mp.dump(TEST_MP_FP)
        loaded_mp = MeshProject.load(TEST_MP_FP)
        self.assertTrue(loaded_mp == mp)


if __name__ == "__main__":
    main()

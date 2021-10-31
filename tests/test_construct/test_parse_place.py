# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.construct.parse_place import PlaceComponent, PlaceFile

DIR = Path(__file__).parent


class TestPlace(TestCase):
    def test_PlaceComponent(self):
        pc = PlaceComponent(
            symbol="A1",
            footprint="EXMPL1",
            side="Top",
            x="1.6000",
            y="0.2300",
            rotation="90",
            glue_x="0",
            glue_y="0",
            glu_dia="0",
            technology="SMD",
            pin_count=1,
        )
        self.assertTrue(pc.x == 1.6)
        self.assertTrue(pc.y == 0.23)
        self.assertTrue(pc.rotation == 90.0)

    def test_PlaceFile(self):
        pf = PlaceFile.load(DIR / "LMP.place")
        self.assertTrue(len(pf.component_list) == 11)
        self.assertIsInstance(pf.component_list[0], PlaceComponent)

    def test_PlaceFile_to_dict(self):
        pf = PlaceFile.load(DIR / "LMP.place")
        pf_dict = pf.dict()
        self.assertTrue("project_name" in pf_dict)
        self.assertTrue("units" in pf_dict)
        self.assertTrue("component_list" in pf_dict)
        self.assertIsInstance(pf_dict["component_list"][0], dict)


if __name__ == "__main__":
    main()

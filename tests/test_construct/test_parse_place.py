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
        )
        self.assertTrue(pc.x == 1.6)
        self.assertTrue(pc.y == 0.23)
        self.assertTrue(pc.rotation == 90.0)

    def test_PlaceFile(self):
        pf = PlaceFile.load(DIR / "LMP.place")
        print(pf)


if __name__ == "__main__":
    main()

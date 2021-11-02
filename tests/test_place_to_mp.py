# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.place_to_mp import main

DIR = Path(__file__).parent
TEMP_DIR = DIR / ".temp"
TEMP_DIR.mkdir(0o777, True, True)


class TestPlace_to_MP(TestCase):
    def test_valid_file_conversion(self):
        main(
            [
                "--place",
                str(DIR / "test_construct" / "LMP.place"),
                "--mp",
                str(TEMP_DIR / "test.mp.yaml"),
            ]
        )

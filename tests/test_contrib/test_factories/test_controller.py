# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.contrib.factories.Controller import Controller
from PyR3.factory import build_and_save
from tests.temp_dir import TEMP_DIR

DIR = Path(__file__).parent


class TestController(TestCase):
    def test_render(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save(
                "python",
                Controller,
                {
                    "box_size": ["1m", "1.5m", "0.3m"],
                    "box_material": {},
                    "bevel_count": 1,
                    "bevel_width": "0.1m",
                    "pinsXY": {},
                    "pins_XY": {},
                    "pinsX_Y": {},
                    "pins_X_Y": {},
                },
                temp_dir / "Controller_0.glb",
            )

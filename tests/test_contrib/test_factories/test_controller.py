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
                    "box_size": ["1.5m", "3m", "0.6m"],
                    "box_material": {"color": "#030303"},
                    "bevel_count": 1,
                    "bevel_width": "0.05m",
                    "box_offset": "0.0m",
                    "pins_aY_posX": {
                        "include": True,
                        "pin_count": 10,
                        "begin_offset": "0.2m",
                        "total_width": "0.6m",
                        "total_height": "0.5m",
                        "total_depth": ".1m",
                        "lower_length": ".2m",
                        "upper_length": ".2m",
                        "steps": 32,
                        "thickness": "0.05m",
                        "material": {
                            "color": "#666",
                            "metallic": 0.8,
                            "roughness": 0.0,
                        },
                    },
                    "pins_aY_negX": {
                        "include": True,
                        "pin_count": 10,
                        "begin_offset": "0.2m",
                        "total_width": "0.6m",
                        "total_height": "0.5m",
                        "total_depth": ".1m",
                        "lower_length": ".2m",
                        "upper_length": ".2m",
                        "steps": 32,
                        "thickness": "0.05m",
                        "material": {
                            "color": "#666",
                            "metallic": 0.8,
                            "roughness": 0.0,
                        },
                    },
                    "pins_aX_posY": {
                        "include": True,
                        "pin_count": 5,
                        "begin_offset": "0.2m",
                        "total_width": "0.6m",
                        "total_height": "0.5m",
                        "total_depth": ".1m",
                        "lower_length": ".2m",
                        "upper_length": ".2m",
                        "steps": 32,
                        "thickness": "0.05m",
                        "material": {
                            "color": "#666",
                            "metallic": 0.8,
                            "roughness": 0.0,
                        },
                    },
                    "pins_aX_negY": {
                        "include": True,
                        "pin_count": 5,
                        "begin_offset": "0.2m",
                        "total_width": "0.6m",
                        "total_height": "0.5m",
                        "total_depth": ".1m",
                        "lower_length": ".2m",
                        "upper_length": ".2m",
                        "steps": 32,
                        "thickness": "0.05m",
                        "material": {
                            "color": "#666",
                            "metallic": 0.8,
                            "roughness": 0.0,
                        },
                    },
                },
                temp_dir / "Controller_0.glb",
            )

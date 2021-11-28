# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase

from PyR3.contrib.factories.CapacitorCase import CapacitorCase
from PyR3.contrib.factories.LCurve import LCurve
from PyR3.contrib.factories.SCurve import SCurve
from PyR3.factory import build_and_save_python
from tests.temp_dir import TEMP_DIR


class TestBatchMeshFactory(TestCase):
    def test_CapacitorCase(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save_python(
                "python",
                CapacitorCase,
                {
                    "h1": "0.3m",
                    "h2": "0.3m",
                    "h3": "1m",
                    "scale": 0.9,
                    "radius": "0.6m",
                    "bevel_width": "0.05m",
                    "bevel_segments": 3,
                    "circle_vertices": 24,
                    "material": {"color": "#F00"},
                },
                temp_dir / "TestCapacitorCylinder_test.glb",
            )

    def test_SCurve(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save_python(
                "python",
                SCurve,
                {
                    "total_width": "1m",
                    "total_height": "1m",
                    "total_depth": ".5m",
                    "lower_length": ".25m",
                    "upper_length": ".25m",
                    "steps": 32,
                    "thickness": "0.1m",
                    "material": {"color": "#33F"},
                },
                temp_dir / "SCurve_test.glb",
            )

    def test_SCurve_asymmetric(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save_python(
                "python",
                SCurve,
                {
                    "total_width": "2m",
                    "total_height": "1m",
                    "total_depth": ".5m",
                    "lower_length": ".2m",
                    "upper_length": ".8m",
                    "steps": 32,
                    "thickness": "0.1m",
                    "material": {"color": "#33F"},
                },
                temp_dir / "SCurve_test_asymmetric.glb",
            )

    def test_LCurve(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save_python(
                "python",
                LCurve,
                {
                    "total_width": "2m",
                    "total_heigh": "2m",
                    "bend": True,
                    "bend_radius": "1m",
                    "bend_segments": 6,
                    "bevel": 3,
                    "bevel_depth": "0.1m",
                    "width": "0.1m",
                    "material": {},
                },
                temp_dir / "LCurve_test.glb",
            )

    def test_LCurve_asymmetric(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save_python(
                "python",
                LCurve,
                {
                    "total_width": "1m",
                    "total_heigh": "2m",
                    "bend": True,
                    "bend_radius": "0.3m",
                    "bend_segments": 6,
                    "width": "0.1m",
                    "bevel": 0,
                    "bevel_depth": 0,
                    "material": {},
                },
                temp_dir / "LCurve_test_asymmetric.glb",
            )

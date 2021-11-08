# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase

from PyR3.contrib import build_and_save
from PyR3.contrib.factories.CapacitorCase import CapacitorCase
from tests.temp_dir import TEMP_DIR


class TestCapacitorCylinder(TestCase):
    def test_instantiate(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save(
                CapacitorCase,
                {
                    "h1": "0.3m",
                    "h2": "0.3m",
                    "h3": "1m",
                    "scale": 0.9,
                    "radius": "0.6m",
                    "bevel_width": "0.05m",
                    "bevel_segments": 3,
                },
                temp_dir / "TestCapacitorCylinder_test_instantiate.glb",
            )

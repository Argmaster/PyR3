# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.contrib.factories.CapacitorCase import CapacitorCase
from PyR3.factory import build_and_save, import_factory
from tests.temp_dir import TEMP_DIR

DIR = Path(__file__).parent


class TestFactorySubpackage(TestCase):
    def test_import_factory(self):
        class_ = import_factory(
            "PyR3.contrib.factories.CapacitorCase.CapacitorCase"
        )
        self.assertEqual(class_, CapacitorCase)

    def test_import_factory_non_factory(self):
        self.assertRaises(TypeError, import_factory, "pathlib.Path")

    def test_build_and_save(self):
        with TEMP_DIR(delete=False) as temp_dir:
            build_and_save(
                "PyR3.contrib.factories.CapacitorCase.CapacitorCase",
                {
                    "h1": "0.3m",
                    "h2": "0.3m",
                    "h3": "1m",
                    "scale": 0.9,
                    "radius": "0.6m",
                    "bevel_width": "0.05m",
                    "bevel_segments": 3,
                    "circle_vertices": 24,
                },
                temp_dir / "TestCapacitorCylinder_test_instantiate.glb",
            )

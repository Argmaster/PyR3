# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from packaging.version import Version

from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0
from PyR3.shortcut.context import Objects, wipeScenes

MI_DIR_PATH = Path(__file__).parent


class TestModelInfo(TestCase):
    def get_default_mi(self):
        return ModelInfoV1_0_0(
            MI_DIR_PATH, "", "1.0.0-beta", "Unknown", "", [], "../test_lib/model.glb"
        )

    def test_no_blend_models_in_library(self):
        self.assertRaises(
            RuntimeError,
            lambda: ModelInfoV1_0_0(
                MI_DIR_PATH,
                "",
                "1.0.0-beta",
                "Unknown",
                "",
                [],
                "../test_lib/model.blend",
            ),
        )

    def test_path_normalization(self):
        mi = self.get_default_mi()
        self.assertEqual(mi.directory, MI_DIR_PATH)

    def test_version(self):
        mi = self.get_default_mi()
        self.assertTrue(mi.version == Version("1.0.0b0"))
        self.assertFalse(mi.version > Version("1.0.0-beta"))
        self.assertTrue(mi.version < Version("1.0.0"))
        self.assertTrue(mi.version > Version("1.0.0-alpha"))
        self.assertTrue(mi.version.public == "1.0.0b0")

    def test_import(self):
        wipeScenes()
        mi = self.get_default_mi()
        self.assertEqual(len(Objects.all()), 0)
        mi.load()
        self.assertEqual(len(Objects.all()), 1)

    def test_calculate_hash(self):
        mi = self.get_default_mi()
        self.assertEqual(mi.hash, "+B4LrpYDjvu3t74iPTBsdYfBbx0=")


if __name__ == "__main__":
    main()

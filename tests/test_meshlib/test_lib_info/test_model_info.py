# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from black import json
from packaging.version import Version

from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0
from PyR3.shortcut.context import Objects, wipeScenes

MI_DIR_PATH = Path(__file__).parent


class TestModelInfo(TestCase):
    def get_default_mi(
        self,
        directory=MI_DIR_PATH,
        hash="",
        version="1.0.0-beta",
        author="Unknown",
        description="",
        tags=["example_tag"],
        file="../test_lib/model1.glb",
    ):
        return ModelInfoV1_0_0(
            directory=directory,
            hash=hash,
            version=version,
            author=author,
            description=description,
            tags=tags,
            icon="__default_icon__",
            file=file,
            scale=1,
        )

    def test_no_blend_models_in_library(self):
        self.assertRaises(
            RuntimeError,
            lambda: self.get_default_mi(file="../test_lib/model.blend"),
        )

    def test_initialization(self):
        self.get_default_mi()

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

    def test_serialization(self):
        mi = self.get_default_mi()
        PARAMS = {
            "hash": "+B4LrpYDjvu3t74iPTBsdYfBbx0=",
            "version": "1.0.0b0",
            "author": "Unknown",
            "description": "",
            "tags": ["example_tag"],
            "icon": "__default_icon__",
            "file": "../test_lib/model1.glb",
            "scale": 1.0,
        }
        self.assertEqual(
            mi.dict(),
            PARAMS,
        )
        self.assertEqual(
            mi.json(),
            json.dumps(PARAMS),
        )

    def test_match_functions(self):
        mi = self.get_default_mi()
        self.assertTrue(mi.match_tag("example_tag"))
        self.assertTrue(mi.match_hash("+B4LrpYDjvu3t74iPTBsdYfBbx0="))

    def test_info_equality(self):
        mi1 = self.get_default_mi()
        mi2 = self.get_default_mi()
        self.assertTrue(mi1 == mi2)
        mi3 = self.get_default_mi(tags=["Example1", "Example2"])
        self.assertFalse(mi1 == mi3)

    def test_with_set_usage(self):
        mi1 = self.get_default_mi()
        mi2 = self.get_default_mi()
        self.assertEqual(len({mi1, mi2}), 1)
        mi3 = self.get_default_mi(tags=["Example1", "Example2"])
        self.assertEqual(len({mi1, mi3}), 2)

# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib import LibraryManager
from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0

DIR = Path(__file__).parent


class TestLibraryManager(TestCase):
    def test_instantiate_with_paths(self):
        paths = ["."]
        lib_mng = LibraryManager(paths)
        self.assertTrue(isinstance(lib_mng.PATH[0], Path))
        self.assertTrue(lib_mng.PATH[0] == Path(paths[0]).resolve())

    def test_find_library(self):
        lib_mng = LibraryManager([DIR / "test_lib"])
        self.assertTrue(len(lib_mng.LIBS) == 1)

    def test_get_by_hash(self):
        lib_mng = LibraryManager([DIR / "test_lib"])
        HASH = "e+kOrn6hL4tcJIHHwYWNLTbhzzY="
        model = lib_mng.get_by_hash(HASH)
        self.assertIsInstance(model, ModelInfoV1_0_0)
        self.assertEqual(model.hash, HASH)
        self.assertRaises(KeyError, lambda: lib_mng.get_by_hash("Some random hash"))

    def test_get_by_tag(self):
        lib_mng = LibraryManager([DIR / "test_lib"])
        models = lib_mng.get_by_tag("CommonTag")
        self.assertTrue(len(models) == 2)
        models = lib_mng.get_by_tag("Example1")
        self.assertTrue(len(models) == 1)
        models = lib_mng.get_by_tag("UserCustomTag2")
        self.assertTrue(len(models) == 1)


if __name__ == "__main__":
    main()

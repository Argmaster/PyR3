# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

import yaml
from black import json
from packaging.version import Version

from PyR3.meshlib.lib_obj.lib_info import LibraryInfoV1_0_0
from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0

FILE_DIR = Path(__file__).parent
LIB_FILE_PATH = FILE_DIR / "../test_lib/__lib__.yaml"
with LIB_FILE_PATH.open("r", encoding="utf-8") as file:
    TEST_LIB_INIT_DATA = yaml.safe_load(file.read())


class TestInfoV1_0_0(TestCase):
    def get_default_li(self):
        return LibraryInfoV1_0_0(
            lib_file_path=LIB_FILE_PATH,
            **TEST_LIB_INIT_DATA,
        )

    def test_LibraryInfoV1_0_0_basic_dispatch(self):
        li = self.get_default_li()
        self.assertTrue(len(li.model_list) == 2)

    def test_LibraryInfoV1_0_0_lib_version(self):
        li = self.get_default_li()
        self.assertTrue(li.lib_version == Version("1.0.0"))
        self.assertFalse(li.lib_version > Version("2.0.0-beta"))
        self.assertTrue(li.lib_version < Version("1.0.2"))
        self.assertTrue(li.lib_version > Version("1.0.0-alpha"))

    def test_LibraryInfoV1_0_0_types(self):
        li = self.get_default_li()
        self.assertIsInstance(li.lib_file_path, Path)
        self.assertIsInstance(li.name, str)
        self.assertIsInstance(li.author, str)
        self.assertIsInstance(li.description, str)
        self.assertIsInstance(li.lib_version, Version)
        self.assertIsInstance(li.model_list, list)
        self.assertIsInstance(li.model_list[0], ModelInfoV1_0_0)

    def test_LibraryInfoV1_0_0_serialization(self):
        li = self.get_default_li()
        print(li.dict())
        print(TEST_LIB_INIT_DATA)
        self.assertEqual(li.dict(), TEST_LIB_INIT_DATA)
        self.assertEqual(
            json.dumps(TEST_LIB_INIT_DATA),
            li.json(),
        )

    def test_LibraryInfoV1_0_0_match(self):
        li = self.get_default_li()
        self.assertIsInstance(
            li.match_hash("+B4LrpYDjvu3t74iPTBsdYfBbx0="), ModelInfoV1_0_0
        )
        self.assertRaises(
            ValueError, lambda: li.match_hash("Some decent hash that doesn't exist")
        )
        self.assertTrue(len(li.match_tag("Any")) == 0, "No matching tags")
        self.assertTrue(len(li.match_tag("Example1")) == 1, "One matching tags")
        print(li.match_tag("Example"))
        self.assertTrue(len(li.match_tag("Example")) == 2, "Two matching tags")


if __name__ == "__main__":
    main()

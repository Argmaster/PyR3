# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib.lib_obj import LibraryObject
from PyR3.meshlib.lib_obj.lib_info import LibraryInfoV1_0_0
from PyR3.meshlib.lib_obj.model_info import ModelInfoBase

from .test_lib_info import LIB_FILE_PATH, TEST_LIB_INIT_DATA

BASE_PATH = Path(__file__).parent


class TestLibraryObject(TestCase):
    def get_default_lo(self):
        return LibraryObject(
            LIB_FILE_PATH,
            **TEST_LIB_INIT_DATA,
        )

    def test_init(self):
        lo = self.get_default_lo()
        self.assertIsInstance(lo.info, LibraryInfoV1_0_0)

    def test_version_not_supported(self):
        self.assertRaises(
            TypeError, lambda: LibraryObject(LIB_FILE_PATH, version="2.0.0")
        )

    def test_str(self):
        lo = self.get_default_lo()
        self.assertEqual(
            str(lo),
            f"""Library[Example Lib 1.0.0 by Krzysztof Wiśniewski at "{LIB_FILE_PATH}"]""",
        )

    def test_save_in_place(self):
        lo = self.get_default_lo()
        lo.save_in_place()

    def test_match_hash(self):
        lo = self.get_default_lo()
        mi = lo.match_hash("e+kOrn6hL4tcJIHHwYWNLTbhzzY=")
        self.assertIsInstance(mi, ModelInfoBase)

    def test_match_tag_from_lib_file(self):
        lo = self.get_default_lo()
        mi_list = lo.match_tag("Example")
        self.assertTrue(len(mi_list) == 2)
        mi_list = lo.match_tag("Example2")
        self.assertTrue(len(mi_list) == 1)
        mi_list = lo.match_tag("Non existing example")
        self.assertTrue(len(mi_list) == 0)

    def test_match_tag_from_user_tags(self):
        lo = self.get_default_lo()
        mi_list = lo.match_tag("UserCustomTag")
        self.assertTrue(len(mi_list) == 2)
        mi_list = lo.match_tag("UserCustomTag1")
        self.assertTrue(len(mi_list) == 1)


if __name__ == "__main__":
    main()

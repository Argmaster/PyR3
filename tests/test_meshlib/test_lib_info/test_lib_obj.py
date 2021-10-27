# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib.lib_obj import LibraryObject
from PyR3.meshlib.lib_obj.lib_info import LibraryInfoV1_0_0

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

    def test_autodump(self):
        lo = self.get_default_lo()
        lo.autodump("yaml")
        lo.autodump("toml")
        lo.autodump("json")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.meshlib.lib_obj import LibraryObject

from .test_lib_info import LIB_FILE_PATH, TEST_LIB_INIT_DATA

BASE_PATH = Path(__file__).parent


class TestLibraryObject(TestCase):
    def get_default_lo(self):
        return LibraryObject(
            LIB_FILE_PATH,
            **TEST_LIB_INIT_DATA,
        )

    def test_LibraryObject_init(self):
        self.get_default_lo()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.meshlib.lib_info.info import LibraryInfoV1_0_0


class TestInfoV1_0_0(TestCase):
    def test_InfoV1_0_0_basic_dispatch(self):
        LibraryInfoV1_0_0(99, 32)


if __name__ == "__main__":
    main()

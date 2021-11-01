# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.place_to_mp import main

DIR = Path(__file__).parent


class TestPlace_to_MP(TestCase):
    def test_valid_file_conversion(self):
        main()

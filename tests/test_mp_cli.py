# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.mp_cli import main

DIR = Path(__file__).parent


class TestMpCLI(TestCase):
    def test_main(self):
        main([str(DIR / "test_construct" / "LMP91200.mp.yaml"), "--check"])

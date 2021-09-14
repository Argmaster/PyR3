# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Length


class TestLength(TestCase):
    def test_Length(self):
        self.assertEqual(Length().digest("3m"), 3)
        self.assertEqual(Length().digest("3m"), 3)

    def test_Length_mixed(self):
        self.assertEqual(Length().digest("3m 4mm"), 3.004)
        self.assertEqual(Length().digest("3in 4mm"), 0.0802)


if __name__ == "__main__":
    main()

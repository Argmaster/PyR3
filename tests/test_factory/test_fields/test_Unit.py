# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Length


class TestLength(TestCase):
    def test_Length(self):
        self.assertEqual(Length("3m").get(), 3)
        self.assertEqual(Length("3mx").get(), 3)

    def test_Length_mixed(self):
        self.assertEqual(Length("3m 4mm").get(), 3.004)
        self.assertEqual(Length("3in 4mm").get(), 0.0802)


if __name__ == "__main__":
    main()

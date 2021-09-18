# -*- coding: utf-8 -*-
from __future__ import annotations
from decimal import Decimal

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Length


class TestLength(TestCase):
    def test_literal(self):
        self.assertEqual(Length().digest("3m"), 3)
        self.assertEqual(Length().digest("3m"), 3)

    def test_literal_mixed(self):
        self.assertEqual(Length().digest(" 3m 4mm  "), 3.004)
        self.assertEqual(Length().digest("3in   ,4mm"), 0.0802)

    def test_decimal(self):
        self.assertEqual(Length().digest(Decimal("3.244")), 3.244)

    def test_float(self):
        self.assertEqual(Length().digest(9.9), 9.9)

    def test_int(self):
        self.assertEqual(Length().digest(99), 99)

    def test_invalid_type(self):
        self.assertRaises(TypeError, lambda: Length().digest(tuple()))

    def test_no_value_error(self):
        self.assertRaises(KeyError, lambda: Length().digest())

    def test_no_value_use_default(self):
        self.assertEqual(Length(default=7).digest(), 7)

    def test_output_unit(self):
        self.assertEqual(Length(output_unit="mm").digest(8), 8000)

if __name__ == "__main__":
    main()

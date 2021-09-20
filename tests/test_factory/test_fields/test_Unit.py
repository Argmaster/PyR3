# -*- coding: utf-8 -*-
from __future__ import annotations
from decimal import Decimal

from unittest import TestCase, main

from PyR3.factory.fields.Unit import Angle, Length


class TestLengthField(TestCase):
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


class TestAngleField(TestCase):
    def test_literal(self):
        self.assertEqual(Angle().digest("3deg"), 0.05235987755982989)
        self.assertEqual(Angle().digest("3rad"), 3)

    def test_literal_mixed(self):
        self.assertEqual(Angle().digest(" 3rad 1π  "), 6.141592653589793)
        self.assertEqual(Angle().digest("3rad   ,1pi"), 6.141592653589793)

    def test_decimal(self):
        self.assertEqual(Angle().digest(Decimal("3.244")), 3.244)

    def test_invalid_type(self):
        self.assertRaises(TypeError, lambda: Angle().digest(tuple()))

    def test_no_value_error(self):
        self.assertRaises(KeyError, lambda: Angle().digest())

    def test_no_value_use_default(self):
        self.assertEqual(Angle(default=7).digest(), 7)

    def test_output_unit(self):
        self.assertEqual(Angle(output_unit="deg").digest(8), 458.3662361046586)
        self.assertRaises(KeyError, lambda: Angle(output_unit="mm").digest(8))


if __name__ == "__main__":
    main()

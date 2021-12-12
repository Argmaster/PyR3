# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase

from PyR3.factory.fields.Number import Boolean, Float, Integer


class TestBooleanFiled(TestCase):
    def test_digest_string_not_boolable(self):
        self.assertRaises(ValueError, lambda: Boolean().digest("i dont care"))

    def test_digest_truthy_string(self):
        self.assertTrue(Boolean().digest("true"))
        self.assertTrue(Boolean().digest("TRuE"))
        self.assertTrue(Boolean().digest("yes"))
        self.assertTrue(Boolean().digest("Y"))
        self.assertTrue(Boolean().digest("T"))
        self.assertTrue(Boolean().digest("1"))

    def test_digest_falsy_string(self):
        self.assertFalse(Boolean().digest("False"))
        self.assertFalse(Boolean().digest("NO"))
        self.assertFalse(Boolean().digest("n"))
        self.assertFalse(Boolean().digest("F"))
        self.assertFalse(Boolean().digest("0"))

    def test_digest_truthy_int(self):
        self.assertTrue(Boolean().digest(1))
        self.assertTrue(Boolean().digest(435))
        self.assertTrue(Boolean().digest(-33))

    def test_digest_falsy_int(self):
        self.assertFalse(Boolean().digest(0))

    def test_digest_other_boolable(self):
        self.assertFalse(Boolean().digest([]))
        self.assertTrue(Boolean().digest([32]))


class TestIntegerField(TestCase):
    def test_digest(self):
        self.assertEqual(Integer().digest("11"), 11)
        self.assertEqual(Integer().digest(11), 11)
        self.assertEqual(Integer().digest(0.11), 0)
        self.assertEqual(Integer().digest(11.0), 11)

    def test_range(self):
        self.assertRaises(
            ValueError,
            lambda: Integer(value_range=range(0, 10, 2)).digest(9),
        )
        self.assertEqual(Integer(value_range=range(0, 10, 2)).digest(6), 6)

    def test_default(self):
        self.assertRaises(KeyError, lambda: Integer().digest(None))
        self.assertEqual(Integer(default=6).digest(None), 6)


class TestFloatField(TestCase):
    def test_digest(self):
        self.assertEqual(Float().digest("11"), 11)
        self.assertEqual(Float().digest(11), 11)
        self.assertEqual(Float().digest(0.11), 0.11)
        self.assertEqual(Float().digest(11.0), 11.0)

    def test_range(self):
        self.assertRaises(ValueError, lambda: Float(min=3.44).digest(3.2))
        self.assertRaises(ValueError, lambda: Float(max=3.44).digest(3.9))
        self.assertEqual(Float(min=3.44, max=3.49).digest(3.46), 3.46)
        self.assertRaises(
            ValueError, lambda: Float(min=3.44, max=3.49).digest(3.55)
        )

    def test_default(self):
        self.assertRaises(KeyError, lambda: Float().digest(None))
        self.assertEqual(Float(default=6).digest(None), 6)

# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main

from PyR3.factory.fields.Number import Float, Integer


class TestIntegerField(TestCase):
    def test_digest(self):
        self.assertEqual(Integer().digest("11"), 11)
        self.assertEqual(Integer().digest(11), 11)
        self.assertEqual(Integer().digest(0.11), 0)
        self.assertEqual(Integer().digest(11.0), 11)

    def test_range(self):
        self.assertRaises(
            ValueError, lambda: Integer(value_range=range(0, 10, 2)).digest(9)
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
        self.assertRaises(ValueError, lambda: Float(min=3.44, max=3.49).digest(3.55))

    def test_default(self):
        self.assertRaises(KeyError, lambda: Float().digest(None))
        self.assertEqual(Float(default=6).digest(None), 6)


if __name__ == "__main__":
    main()

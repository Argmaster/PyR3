# -*- coding: utf-8 -*-
from __future__ import annotations
from PyR3.factory.fields.Struct import Struct
from PyR3.factory.fields.Number import Integer
from unittest import TestCase, main


class TestStructField(TestCase):
    def test_digest(self):
        class Color(Struct):
            R = Integer(value_range=range(0, 255))
            G = Integer(value_range=range(0, 255))
            B = Integer(value_range=range(0, 255))

        namespace = Color().digest(
            {
                "R": 200,
                "G": 100,
                "B": 150,
            }
        )
        self.assertTrue(hasattr(namespace, "R"))
        self.assertTrue(hasattr(namespace, "G"))
        self.assertTrue(hasattr(namespace, "B"))

    def test_digest_field_fails(self):
        class Color(Struct):
            R = Integer(value_range=range(0, 255))
            G = Integer(value_range=range(0, 255))
            B = Integer(value_range=range(0, 255))

        self.assertRaises(
            ValueError,
            lambda: Color().digest(
                {
                    "R": 200,
                    "G": 300,
                    "B": 150,
                }
            ),
        )


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main

from PyR3.factory.fields.Number import Integer


class TestIntegerField(TestCase):

    def test_digest(self):
        self.assertEqual(Integer().digest("11"), 11)
        self.assertEqual(Integer().digest(11), 11)
        self.assertEqual(Integer().digest(11.0), 11)

    def test_range(self):
        self.assertRaises(ValueError, lambda: Integer(value_range=range(0, 10, 2)).digest(9))

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
from __future__ import annotations
from PyR3.factory.fields.Select import Select
from unittest import TestCase, main


class TestSelectField(TestCase):
    def test_digest(self):
        self.assertEqual(Select("ONE", "TWO", "THREE").digest("TWO"), "TWO")

    def test_digest_default(self):
        self.assertEqual(Select("ONE", "TWO", "THREE", default_index=0).digest(), "ONE")

    def test_digest_key_error(self):
        self.assertRaises(KeyError, lambda: Select("ONE", "TWO", "THREE").digest())


if __name__ == "__main__":
    main()

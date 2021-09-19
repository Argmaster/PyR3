# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from PyR3.factory.fields.String import Regex, String
from unittest import TestCase, main


class TestString(TestCase):
    def test_digest(self):
        s0 = "Some random string"
        self.assertEqual(String().digest(s0), s0)

    def test_digest_min_max(self):
        s0 = "a" * 5
        self.assertRaises(ValueError, lambda: String(min_length=6).digest(s0))
        self.assertEqual(String(min_length=5).digest(s0), s0)
        self.assertRaises(ValueError, lambda: String(max_length=4).digest(s0))
        self.assertEqual(String(max_length=5).digest(s0), s0)

    def test_digest_default(self):
        self.assertEqual(String(default="abc").digest(), "abc")


class TestRegex(TestCase):
    def test_digest(self):
        self.assertEqual(Regex(r"a+").digest("aaa"), "aaa")
        self.assertEqual(Regex(re.compile(r"a+")).digest("aaa"), "aaa")

    def test_invalid_pattern_type(self):
        self.assertRaises(TypeError, lambda: Regex([]))

    def test_digest_not_matching(self):
        self.assertRaises(ValueError, lambda: Regex(r"a+").digest("aab"))

    def test_use_default(self):
        self.assertEqual(Regex(r"a+", default="bbb").digest(), "bbb")


if __name__ == "__main__":
    main()

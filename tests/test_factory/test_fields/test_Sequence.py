# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.factory.fields.Number import Float, Integer
from PyR3.factory.fields.Sequence import HeterotypeSequence, HomotypeSequence
from PyR3.factory.fields.String import String

DIR = Path(__file__).parent


class TestHeterotypeSequence(TestCase):
    def test_digest_default(self):
        self.assertEqual(
            HeterotypeSequence(
                Float(min=0.0, max=1.0),
                Integer(value_range=range(1, 10)),
                String(),
                default=[0.44, 5, "Ala ma kota"],
            ).digest(None),
            (0.44, 5, "Ala ma kota"),
        )

    def test_digest_default_too_many_args(self):
        self.assertRaises(
            ValueError,
            HeterotypeSequence,
            Float(min=0.0, max=1.0),
            default=[0.44, 5, "Ala ma kota"],
        )

    def test_digest_no_default(self):
        self.assertRaises(
            KeyError, HeterotypeSequence(Float(min=0.0, max=1.0)).digest, None
        )

    def test_digest_default_field_validation_failure(self):
        self.assertRaises(
            ValueError,
            HeterotypeSequence,
            Float(min=0.0, max=1.0),
            default=["nie float"],
        )


class TestHomotypeSequence(TestCase):
    def test_with_default(self):
        self.assertEqual(
            HomotypeSequence(Float(), default=(3.33, 23.1, 53)).digest(None),
            (3.33, 23.1, 53),
        )

    def test_without_default(self):
        self.assertRaises(KeyError, HomotypeSequence(Float()).digest, None)

    def test_force_length(self):
        self.assertRaises(
            ValueError,
            HomotypeSequence(Float(), length=3).digest,
            (33, 23.2),
        )

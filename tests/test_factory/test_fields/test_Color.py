# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.factory.fields.Color import Color, parse_hex_color, parse_rgb_color

DIR = Path(__file__).parent


class TestColorField(TestCase):
    def test_hex_rgb_color(self):
        self.assertEqual(parse_hex_color("#FF00FF"), [255, 0, 255])
        self.assertEqual(parse_hex_color("#F0F"), [255, 0, 255])

    def test_hex_rgba_color(self):
        self.assertEqual(parse_hex_color("#FF00FFAA"), [255, 0, 255, 170])
        self.assertEqual(parse_hex_color("#F0FA"), [255, 0, 255, 170])
        self.assertEqual(parse_hex_color("#FCBA1233"), [252, 186, 18, 51])

    def test_hex_fail_color(self):
        self.assertEqual(parse_hex_color("#FF00FG"), None)
        self.assertEqual(parse_hex_color("#FF00FF0"), None)
        self.assertEqual(parse_hex_color("#FF00F"), None)
        self.assertEqual(parse_hex_color("#XX00C"), None)
        self.assertEqual(parse_hex_color("#FCBA120033"), None)

    def test_rgb_rgb_color(self):
        self.assertEqual(parse_rgb_color("rgb(255, 0, 255)"), [255, 0, 255])
        self.assertEqual(
            parse_rgb_color("rgb(  255,   0, 255 )"), [255, 0, 255]
        )
        self.assertEqual(parse_rgb_color("rgb(  255   0 255 )"), [255, 0, 255])
        self.assertEqual(parse_rgb_color("rgb(255 0 255)"), [255, 0, 255])
        self.assertEqual(parse_rgb_color("rgb(255, 0 255)"), [255, 0, 255])

    def test_rgb_rgba_color(self):
        self.assertEqual(
            parse_rgb_color("rgba(255, 0, 255, 170)"), [255, 0, 255, 170]
        )
        self.assertEqual(
            parse_rgb_color("rgba(  255,   0, 255   ,170)"), [255, 0, 255, 170]
        )
        self.assertEqual(
            parse_rgb_color("rgba(  255   0 255 170)"), [255, 0, 255, 170]
        )
        self.assertEqual(
            parse_rgb_color("rgba(255 0 255 170)"), [255, 0, 255, 170]
        )
        self.assertEqual(
            parse_rgb_color("rgba(255, 0 255, 170)"), [255, 0, 255, 170]
        )

    def test_Color_field_default(self):
        self.assertEqual(
            Color(default="#FFAA22").digest(None), [255, 170, 34, 255]
        )

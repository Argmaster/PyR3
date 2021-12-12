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

    def test_rgb_color_out_of_range(self):
        self.assertRaises(ValueError, parse_rgb_color, "rgb(345, 546, 170)")

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

    def test_rgb_rgba_color_not_matching(self):
        self.assertEqual(parse_rgb_color("5hg32315b5h3"), None)

    def test_rgba_color_out_of_range(self):
        self.assertRaises(ValueError, parse_rgb_color, "rgba(345, 0 255, 170)")

    def test_Color_field_default_hex(self):
        self.assertEqual(
            Color(default="#FFAA22", do_normalize=False, use_type=list).digest(
                None
            ),
            [255, 170, 34, 255],
        )

    def test_Color_field_fail_with_no_default(self):
        self.assertRaises(
            KeyError,
            lambda: Color(include_alpha=False).digest(None),
        )

    def test_Color_field_digest_hex(self):
        self.assertEqual(
            Color(include_alpha=False, do_normalize=False).digest("#AD2F43"),
            (173, 47, 67),
        )

    def test_Color_field_digest_rgb(self):
        self.assertEqual(
            Color(do_normalize=False).digest("rgba(255, 0 255, 170)"),
            (255, 0, 255, 170),
        )

    def test_Color_field_digest_invalid_syntax(self):
        self.assertRaises(
            SyntaxError,
            Color(include_alpha=False, do_normalize=False).digest,
            "some fancy dancy string",
        )

    def test_Color_field_digest_list(self):
        self.assertEqual(
            Color(include_alpha=False, do_normalize=True).digest(
                [233, 123, 32, 99]
            ),
            (0.9137254901960784, 0.4823529411764706, 0.12549019607843137),
        )

    def test_Color_field_digest_list_too_long(self):
        self.assertRaises(
            ValueError,
            Color(include_alpha=False, do_normalize=False).digest,
            [233, 123, 32, 99, 34, 66],
        )

    def test_Color_field_digest_list_out_of_range(self):
        self.assertRaises(
            ValueError, Color(do_normalize=False).digest, [233, 567, 32, 99]
        )

    def test_Color_field_digest_dict(self):
        self.assertEqual(
            Color(include_alpha=True, do_normalize=False).digest(
                {"R": 212, "G": 233, "B": 32}
            ),
            (212, 233, 32, 255),
        )

    def test_Color_field_digest_invalid_type(self):
        self.assertRaises(
            TypeError,
            Color(include_alpha=True, do_normalize=False).digest,
            3333,
        )

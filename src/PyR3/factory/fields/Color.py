# -*- coding: utf-8 -*-
import re
from functools import partial
from typing import Any, Dict, List, Optional

from .Field import Field


def check_if_in_color_range(value: int) -> int:
    if 0 <= value <= 255:
        return value
    else:
        raise ValueError(f"Value {value} in color out of range [0, 255].")


def parse_hex_color(
    value: str,
    *,
    hex_rgb_short_pattern: re.Pattern,
    hex_rgb_pattern: re.Pattern,
    hex_rgba_short_pattern: re.Pattern,
    hex_rgba_pattern: re.Pattern,
) -> Optional[List[int]]:
    if match := hex_rgb_short_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            int(groupdict.get(color) * 2, base=16) for color in ("R", "G", "B")
        ]
    if match := hex_rgb_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            int(groupdict.get(color), base=16) for color in ("R", "G", "B")
        ]
    if match := hex_rgba_short_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            int(groupdict.get(color) * 2, base=16)
            for color in ("R", "G", "B", "A")
        ]
    if match := hex_rgba_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            int(groupdict.get(color), base=16)
            for color in ("R", "G", "B", "A")
        ]
    else:
        return None


parse_hex_color = partial(
    parse_hex_color,
    hex_rgb_short_pattern=re.compile(
        r"#"
        r"(?P<R>[0-9A-Fa-f]{1})"
        r"(?P<G>[0-9A-Fa-f]{1})"
        r"(?P<B>[0-9A-Fa-f]{1})"
    ),
    hex_rgb_pattern=re.compile(
        r"#"
        r"(?P<R>[0-9A-Fa-f]{2})"
        r"(?P<G>[0-9A-Fa-f]{2})"
        r"(?P<B>[0-9A-Fa-f]{2})"
    ),
    hex_rgba_short_pattern=re.compile(
        r"#"
        r"(?P<R>[0-9A-Fa-f]{1})"
        r"(?P<G>[0-9A-Fa-f]{1})"
        r"(?P<B>[0-9A-Fa-f]{1})"
        r"(?P<A>[0-9A-Fa-f]{1})"
    ),
    hex_rgba_pattern=re.compile(
        r"#"
        r"(?P<R>[0-9A-Fa-f]{2})"
        r"(?P<G>[0-9A-Fa-f]{2})"
        r"(?P<B>[0-9A-Fa-f]{2})"
        r"(?P<A>[0-9A-Fa-f]{2})"
    ),
)


def parse_rgb_color(
    value: str,
    *,
    rgb_pattern: re.Pattern,
    rgba_pattern: re.Pattern,
) -> List[int]:
    if match := rgb_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            check_if_in_color_range(int(groupdict.get(color)))
            for color in ("R", "G", "B")
        ]
    elif match := rgba_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [
            check_if_in_color_range(int(groupdict.get(color)))
            for color in ("R", "G", "B", "A")
        ]
    else:
        return None


parse_rgb_color = partial(
    parse_rgb_color,
    rgb_pattern=re.compile(
        r"rgb\("
        r"\s*(?P<R>[0-9]{1,3})\s*,*"
        r"\s*(?P<G>[0-9]{1,3})\s*,*"
        r"\s*(?P<B>[0-9]{1,3})\s*,*"
        r"\)"
    ),
    rgba_pattern=re.compile(
        r"rgba\("
        r"\s*(?P<R>[0-9]{1,3})\s*,*"
        r"\s*(?P<G>[0-9]{1,3})\s*,*"
        r"\s*(?P<B>[0-9]{1,3})\s*,*"
        r"\s*(?P<A>[0-9]{1,3})\s*,*"
        r"\)"
    ),
)


class Color(Field):
    def __init__(
        self,
        *,
        default: Any = None,
        do_normalize: bool = False,
        use_type: bool = tuple,
        include_alpha: bool = True,
    ) -> None:
        self.do_normalize = do_normalize
        self.use_type = use_type
        self.include_alpha = include_alpha
        if default is not None:
            self.default = self.clean_value(default)

    def digest(self, value: str = None):
        if value is None:
            return self.get_default()
        else:
            return self.clean_value(value)

    def clean_value(self, value):
        color = self.convert_to_list(value)
        color = self.pop_or_pad_to_4(color)
        color = self.apply_alpha_preference(color)
        if self.do_normalize:
            color = self.normalize(color)
        return self.use_type(color)

    def convert_to_list(self, value):
        if isinstance(value, str):
            return self.parse_str_color(value)
        elif isinstance(value, (list, tuple)):
            return self.validate_list_color(value)
        elif isinstance(value, dict):
            return self.validate_dict_color(value)
        else:
            raise TypeError(f"Invalid color value type {type(value)}")

    def parse_str_color(self, value: str):
        if color := parse_hex_color(value):
            return color
        elif color := parse_rgb_color(value):
            return color
        else:
            raise SyntaxError(f"'{value}' is not a valid color literal.")

    def validate_list_color(self, value: List[Any]):
        if 3 <= len(value) <= 4:
            return [check_if_in_color_range(int(v)) for v in value]
        else:
            raise ValueError(
                f"Sequence given has invalid length: {len(value)} (should be 3 or 4)"
            )

    def validate_dict_color(self, value: Dict[str, int]):
        return [
            check_if_in_color_range(value["R"]),
            check_if_in_color_range(value["G"]),
            check_if_in_color_range(value["B"]),
            check_if_in_color_range(value.get("A", 255)),
        ]

    def pop_or_pad_to_4(self, color: List[int]) -> List[int]:
        if len(color) > 4:
            return color[:4]
        elif len(color) < 4:
            zeros = [0 for _ in range(3 - len(color))]
            return color + zeros + [255]
        return color

    def apply_alpha_preference(self, color: List[int]) -> None:
        if not self.include_alpha:
            return color[:3]
        return color

    def normalize(
        self,
        color: List[int],
    ) -> List[float]:
        return [c / 255 for c in color]

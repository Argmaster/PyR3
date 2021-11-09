# -*- coding: utf-8 -*-
import re
from functools import partial
from typing import Any, Dict, List, Optional

from .Field import Field


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
        return [int(groupdict.get(color)) for color in ("R", "G", "B")]
    elif match := rgba_pattern.fullmatch(value):
        groupdict = match.groupdict()
        return [int(groupdict.get(color)) for color in ("R", "G", "B", "A")]
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
        default: Any,
        do_normalize: bool = True,
        use_type: bool = tuple,
        include_alpha: bool = True,
    ) -> None:
        self.do_normalize = do_normalize
        self.use_type = use_type
        self.include_alpha = include_alpha
        self.default = self.clean_color(default)

    def digest(self, value: str = None):
        if value is None:
            return self._get_default()
        else:
            return self.clean_color(value)

    def clean_color(self, value):
        color = self.convert_to_list(value)
        self.apply_alpha_preference(color)
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
            raise RuntimeError(f"Invalid color value type {type(value)}")

    def parse_str_color(self, value: str):
        if color := parse_hex_color(value):
            return color
        elif color := parse_rgb_color(value):
            return color
        else:
            raise SyntaxError(f"'{value}' is not a valid color literal.")

    def validate_list_color(self, value: List[Any]):
        if 3 <= len(value) <= 4:
            return [int(v) for v in value]
        else:
            raise ValueError(
                f"Sequence given has invalid length: {len(value)} (should be 3 or 4)"
            )

    def validate_dict_color(self, value: Dict[str, int]):
        return [value["R"], value["G"], value["B"], value.get("A", 255)]

    def apply_alpha_preference(self, color: List[int]) -> None:
        if self.include_alpha:
            if len(color) <= 3:
                color.extend((255,) * (4 - len(color)))
        else:
            while len(color) >= 4:
                color.pop()

    def normalize(
        self,
        color: List[int],
    ) -> List[float]:
        return [c / 255 for c in color]

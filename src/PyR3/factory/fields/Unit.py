# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import re
from numbers import Number
from typing import List
from typing import Tuple

from .Field import Field


class _SuffixParser:

    _float_regex = r"(?P<VALUE>[\-+]?[0-9]*\.?[0-9]+)"
    tokens: List[re.Pattern, float]
    suffixes: List[str]

    def __init__(self, suffix_to_value: Tuple[Tuple[str, float]]) -> None:
        self.tokens = []
        self.suffixes = []
        for suffix, multiplier in suffix_to_value:
            self.suffixes.append(suffix)
            token = re.compile(f"{self._float_regex}{suffix}")
            self.tokens.append((token, multiplier))

    def parse(self, string: str) -> float:
        total = 0
        index = 0
        while index < len(string):
            for token, multiplier in self.tokens:
                token: re.Pattern
                if match := token.match(string, pos=index):
                    total += float(match.groupdict()["VALUE"]) * multiplier
                    index = match.end()
                    break
            else:
                index += 1
        return total

    def __str__(self) -> str:
        return f"SuffixParser, suffixes: {self.suffixes}"

    __repr__ = __str__


class Length(Field):
    """Accepts float with optional length unit suffix. Unit suffix causes
    float value to be converted to value with unit denoted by `output_unit`.

    Valid unit suffixes are:

        - **mil**  for mils

        - **in**   for inches

        - **ft**   for feets

        - **mm**   for millimeters

        - **cm**   for centimeters

        - **dm**   for decimeters

        - **m**    for meters

    Signs that doesn't match anything are ignored and treated as separators.
    """

    _suffix_to_value_map = (
        ("mil", 2.54 * 1e-5),
        ("in", 0.0254),
        ("ft", 0.3048),
        ("mm", 0.001),
        ("cm", 0.01),
        ("dm", 0.1),
        ("m", 1),
        ("", 1),
    )

    parser = _SuffixParser(_suffix_to_value_map)
    _suffix_to_value_map = dict(_suffix_to_value_map)

    def __init__(
        self,
        *,
        output_unit: str = "m",
        default: str | Number = None,
    ) -> None:
        self.output_divider = self._suffix_to_value_map[output_unit]
        if default is not None:
            self.default = self._digest_value(default)
        else:
            self.default = None

    def _digest_value(self, value: str | Number) -> float:
        if isinstance(value, str):
            return self.parser.parse(value)
        elif isinstance(value, Number):
            return float(value)
        else:
            self._raise_invalid_value_type(value)

    def digest(self, literal: str | Number = None) -> float:
        """Returns total value contained in the literal in meters.

        :param literal: literal to consume or Number
        :type literal: Union[str, Number]
        :raises TypeError: If other type than str or Number is given.
        :raises KeyError: If value is None and no default is given.
        :return: total in meters.
        :rtype: float
        """
        if literal is None:
            value = self._get_default()
        else:
            value = self._digest_value(literal)
        return self._convert_to_output_unit(value)

    def _convert_to_output_unit(self, value: float) -> float:
        return value / self.output_divider


class Angle(Length):
    """Accepts float with optional angle unit suffix. Unit suffix causes
    float value to be converted to value with unit denoted by `output_unit`.

    Valid unit suffixes are:

        - **rad** for radians

        - **π** / **pi** for radians, multiplied by π (3.14...)

        - **deg** for degrees

        - **"** / **sec**  for seconds of angle

        - **'** / **min**  for minutes of angle

    Signs that doesn't match anything are ignored and treated as separators.
    """

    _suffix_to_value_map = (
        ('"', math.pi / (3600 * 180)),
        ("sec", math.pi / (3600 * 180)),
        ("'", math.pi / (60 * 180)),
        ("min", math.pi / (60 * 180)),
        ("°", math.pi / 180),
        ("deg", math.pi / 180),
        ("π", math.pi),
        ("pi", math.pi),
        ("rad", 1),
        ("", 1),
    )

    parser = _SuffixParser(_suffix_to_value_map)
    _suffix_to_value_map = dict(_suffix_to_value_map)

    def __init__(
        self, *, output_unit: str = "rad", default: str | Number = None
    ) -> None:
        super().__init__(output_unit=output_unit, default=default)

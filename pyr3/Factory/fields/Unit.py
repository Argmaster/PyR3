# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from numbers import Number
from typing import List
from .FieldABC import Field


class _LiteralParser:

    tokens: List[re.Pattern, float]

    def __init__(self, *token_multiplier: List[str, float]) -> None:
        self.tokens = []
        for token, multiplier in token_multiplier:
            token = re.compile(token)
            self.tokens.append((token, multiplier))

    def parse(self, string: str) -> float:
        total = 0
        index = 0
        while index < len(string):
            for token, multiplier in self.tokens:
                token: re.Pattern
                if match := token.match(string):
                    total += float(match.groupdict()["VALUE"]) * multiplier
                    index = match.endpos
                    break
            else:
                index += 1
        return total


_float_regex = r"(?P<VALUE>[\-+]?[0-9]*\.?[0-9]+)"


class Length(Field):

    parser = _LiteralParser(
        [f"{_float_regex}mil", 2.54 * 1e-5],
        [f"{_float_regex}in", 0.0254],
        [f"{_float_regex}ft", 0.3048],
        [f"{_float_regex}mm", 0.001],
        [f"{_float_regex}cm", 0.01],
        [f"{_float_regex}dm", 0.1],
        [f"{_float_regex}m", 1],
        [f"{_float_regex}", 1],
    )

    def __init__(self, literal: str|Number) -> None:
        """Parse float literal with units. Literal can contain multiple
        float-unit pairs, not necessarily separated. Output value will be
        equal to sum of all values. In case Number (float, int etc.) is given
        it is assumed that unit is meters.

        Valid units are:

            - **mil**  for mils

            - **in**   for inches

            - **ft**   for feets

            - **mm**   for millimeters

            - **cm**   for centimeters

            - **dm**   for decimeters

            - **m**    for meters

        Signs that doesn't match anything are ignored and treated as separators.
        **Output value is in meters.**

        :param literal: literal to consume or Number
        :type literal: Union[str, Number]
        :raises TypeError: If other type than listed above is given.
        """
        if isinstance(literal, str):
            self.__value = self.parser.parse(literal)
        elif isinstance(literal, Number):
            self.__value = float(literal)
        else:
            raise TypeError(f"Type {type(literal)} of {literal} not supported.")

    def get(self) -> float:
        """Returns total value contained in the literal in meters.

        :return: total in meters.
        :rtype: float
        """
        return self.__value



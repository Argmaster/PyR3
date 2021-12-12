# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from .Field import Field


class Boolean(Field):

    _true_values = {
        "true",
        "yes",
        "y",
        "t",
        "1",
    }
    _false_values = ["false", "no", "n", "f", "0"]

    def clean_value(self, value: Any = None) -> Any:
        if isinstance(value, str):
            value = value.lower()
            if value in self._true_values:
                return True
            elif value in self._false_values:
                return False
            else:
                raise ValueError(
                    f"Can't determine logical value of '{value}'."
                )
        if isinstance(value, (bool, int, float)):
            return value != 0
        else:
            return bool(value)


class Integer(Field):
    def __init__(
        self,
        *,
        default: int = None,
        value_range: range = None,
        not_null: bool = False,
    ) -> None:
        self.value_range = value_range
        self.not_null = not_null
        if default is not None:
            self.default = self.clean_value(default)

    def clean_value(self, value):
        parsed_int = int(value)
        self.check_if_in_range(parsed_int)
        return parsed_int

    def check_if_in_range(self, parsed_int):
        if self.value_range is not None:
            if parsed_int not in self.value_range:
                raise ValueError(
                    f"Value {parsed_int} out of desired value range in {self._trace_location()}."
                )
        if self.not_null:
            if parsed_int == 0:
                raise ValueError("Value can't be null.")


class Float(Field):
    def __init__(
        self,
        *,
        default: float = None,
        min: float = None,
        max: float = None,
        not_null: bool = False,
    ) -> None:
        self.min = min
        self.max = max
        self.not_null = not_null
        if default is not None:
            self.default = self.clean_value(default)

    def clean_value(self, value):
        parsed_float = float(value)
        self.check_if_in_range(parsed_float)
        return parsed_float

    def check_if_in_range(self, parsed_float):
        if self.min is not None:
            if not (self.min <= parsed_float):
                raise ValueError(
                    f"Value {parsed_float} below expected range. (min: {self.min}) in {self._trace_location()}"
                )
        if self.max is not None:
            if not (parsed_float <= self.max):
                raise ValueError(
                    f"Value {parsed_float} above expected range. (max: {self.max}) in {self._trace_location()}"
                )
        if self.not_null:
            if parsed_float == 0:
                raise ValueError("Value can't be null.")

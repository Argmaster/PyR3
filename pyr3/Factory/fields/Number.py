# -*- coding: utf-8 -*-
from __future__ import annotations
from numbers import Number
from PyR3.factory.fields.FieldABC import Field


class Integer(Field):
    def __init__(self, *, default: int = None, value_range: range = None) -> None:
        self.default = default
        self.value_range = value_range

    def digest(self, value: str | Number) -> None:
        if value is None:
            if self.default:
                return self.default
            else:
                self.raise_missing_factory_field()
        else:
            parsed_int = int(value)
            self.check_if_in_range(parsed_int)
            return parsed_int

    def check_if_in_range(self, parsed_int):
        if self.value_range is not None:
            if parsed_int not in self.value_range:
                raise ValueError("Value out of desired value range.")

# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from .Field import Field


class Select(Field):
    def __init__(self, *values, default: int = None) -> None:
        self.values = values
        if default is not None:
            self.default = default

    def digest(self, value: Any = None) -> Any:
        if value is None:
            return self.values[self.get_default()]
        else:
            return self.clean_value(value)

    def clean_value(self, value: Any = None) -> None:
        if value in self.values:
            return value
        else:
            raise ValueError(
                f"Invalid value for {self._trace_location()}, must be one of {self.values}"
            )

# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from .Field import Field


class Select(Field):
    def __init__(self, *values, default_index: int = None) -> None:
        self.values = values
        self.default_index = default_index

    def digest(self, value: Any = None) -> None:
        if value is None:
            if self.default_index is not None:
                return self.values[self.default_index]
            else:
                self._raise_missing_factory_field()
        elif value in self.values:
            return value
        else:
            raise ValueError(
                f"Invalid value for {self._trace_location()}, must be one of {self.values}"
            )

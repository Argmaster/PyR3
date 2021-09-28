# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any


class Field(ABC):

    _field_name: str = "Unknown"
    _factory_name: str = "Unknown"

    @abstractmethod
    def __init__(self, **kwargs) -> None:
        ...

    @abstractmethod
    def digest(self, value: Any = None) -> None:
        ...

    def raise_missing_factory_field(self):
        raise KeyError(f"Missing Factory Field parameter for x{self.trace_location()}.")

    def raise_invalid_value_type(self, value: Any = None):
        if value is None:
            raise TypeError(f"Value of invalid type given to {self.trace_location()}.")
        else:
            raise TypeError(
                f"Value '{value}', type '{type(value)}' is not valid in {self.trace_location()}."
            )

    def set_trace_info(self, _field_name: str, _factory_name: str):
        self._field_name = _field_name
        self._factory_name = _factory_name

    def _get_default(self):
        if self.default:
            return self.default
        else:
            self.raise_missing_factory_field()

    def trace_location(self):
        return f"{self._factory_name}::{self._field_name}"

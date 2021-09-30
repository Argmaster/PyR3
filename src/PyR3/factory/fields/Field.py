# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
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

    def _raise_missing_factory_field(self):
        raise KeyError(
            f"Missing Factory Field parameter for x{self._trace_location()}."
        )

    def _raise_invalid_value_type(self, value: Any = None):
        if value is None:
            raise TypeError(f"Value of invalid type given to {self._trace_location()}.")
        else:
            raise TypeError(
                f"Value '{value}', type '{type(value)}' is not valid in {self._trace_location()}."
            )

    def _set_trace_info(self, _field_name: str, _factory_name: str):
        self._field_name = _field_name
        self._factory_name = _factory_name

    def _get_default(self):
        if self.default:
            return self.default
        else:
            self._raise_missing_factory_field()

    def _trace_location(self):
        return f"{self._factory_name}::{self._field_name}"

    def __str__(self):
        return f"{self.__class__.__qualname__} Field"

    __repr__ = __str__

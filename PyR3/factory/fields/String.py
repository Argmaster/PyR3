# -*- coding: utf-8 -*-
from __future__ import annotations
from .FieldABC import Field


class String(Field):

    def __init__(self, *, default: str=None, min_length: int=None, max_length: int=None) -> None:
        self.default = default
        self.min_length = min_length
        self.max_length = max_length

    def digest(self, value: str = None) -> None:
        if value is None:
            return self._get_default()
        else:
            string = str(value)
            self.check_if_in_range(string)
            return string

    def check_if_in_range(self, string: str):
        if self.min_length is not None:
            if not (self.min_length <= len(string)):
                raise ValueError(f"String for {self.trace_location()} is too short ({len(string)}, min length: {self.min_length})")
        if self.max_length is not None:
            if not (len(string) <= self.max_length):
                raise ValueError(f"String for {self.trace_location()} is too long ({len(string)}, min length: {self.max_length})")
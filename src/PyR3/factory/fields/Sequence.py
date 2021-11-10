# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Sequence, Tuple, Type

from .Field import Field


class HeterotypeSequence(Field):
    def __init__(
        self,
        *subfields: Tuple[Field],
        default: Tuple = None,
        use_type: Type[Sequence] = tuple,
    ) -> None:
        self.subfields = subfields
        self.use_type = use_type
        if default is not None:
            self.default = self.clean_value(default)

    def clean_value(self, value: list | tuple = None) -> None:
        if len(value) != len(self.subfields):
            raise ValueError(
                f"Length of given sequence ({len(value)}) is different from desired ({len(self.subfields)})."
            )
        cleaned_values = []
        for index, dirty_value in enumerate(value):
            field_validator = self.subfields[index]
            cleaned_values.append(
                field_validator.digest(dirty_value),
            )
        return self.use_type(cleaned_values)


class HomotypeSequence(Field):
    def __init__(
        self,
        contained_type: Field,
        *,
        length: int = None,
        default: Tuple = None,
        use_type: Type[Sequence] = tuple,
    ) -> None:
        self.contained_type = contained_type
        self.length = length
        self.use_type = use_type
        if default is not None:
            self.default = self.clean_value(default)

    def clean_value(self, value: list | tuple = None) -> None:
        if self.length is not None and len(value) != self.length:
            raise ValueError(
                f"Length of given sequence ({len(value)}) is "
                f"different from desired ({self.length})."
            )
        cleaned_values = []
        for dirty_value in value:
            cleaned_values.append(
                self.contained_type.digest(dirty_value),
            )
        return self.use_type(cleaned_values)

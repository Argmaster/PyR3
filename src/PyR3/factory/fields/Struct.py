# -*- coding: utf-8 -*-
from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Callable

from PyR3.factory.MeshFactory import MeshFactory, getfields

from .Field import Field


class StructNamespace(dict):
    def __init__(self):
        super().__setitem__("memory", {})

    def __getattr__(self, __name: str) -> Any:
        return super().__getitem__("memory")[__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__getitem__("memory")[__name] = __value

    def dict(self):
        return super().__getitem__("memory").copy()


class Struct(Field):
    """Parent class allowing to create custom struct classes grouping other
    field types by subclassing Struct in body of MeshFactory or another Strut
    field.

    Struct field value is a SimpleNamespace.
    """

    __init = False

    def __new__(cls: Struct, *args, **kwargs) -> Struct:
        if cls.__init is False:
            fields = MeshFactory.get_custom_fields_dict(
                cls.__qualname__, cls.__dict__
            )
            setattr(cls, "__factory_fields__", fields)
            cls.__del_fields(cls, fields)
            cls.__init = True
        return super().__new__(cls)

    def __del_fields(cls, fields):
        for key in fields:
            delattr(cls, key)

    def __init__(self, *, default: Any = None) -> None:
        if default is not None:
            setattr(self, "$default", self.clean_value(default))

    def get_default(self):
        if hasattr(self, "$default"):
            return getattr(self, "$default")
        else:
            self._raise_missing_factory_field()

    def _get_container(self) -> Any:
        return StructNamespace()

    def _get_setter_function(self) -> Callable:
        return setattr

    def clean_value(self, params: dict = None) -> SimpleNamespace:
        """Consumes dictionary of values and returns SimpleNamespace containing
        cleaned values of fields. Redundant params will be ignored. If a value
        is missing, None will be passed to coresponding field.

        :param params: dictionary of values, defaults to None
        :type params: dict, optional
        :return: namespace with cleaned values.
        :rtype: SimpleNamespace
        """
        namespace = self._get_container()
        setter_function = self._get_setter_function()
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            cleaned_value = field.digest(param_value)
            setter_function(namespace, name, cleaned_value)
        return namespace

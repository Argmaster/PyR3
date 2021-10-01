# -*- coding: utf-8 -*-
from __future__ import annotations

from types import SimpleNamespace

from PyR3.factory.MeshFactory import MeshFactory
from PyR3.factory.MeshFactory import getfields

from .Field import Field


class Struct(Field):
    """Parent class allowing to create custom struct classes grouping
    other field types by subclassing Struct in body of MeshFactory or
    another Strut field. Struct field value is a SimpleNamespace.

    """

    __instance: Struct = None

    def __new__(cls: Struct) -> Struct:
        if cls.__instance is None:
            fields = MeshFactory.get_field_names(cls.__qualname__, cls.__dict__)
            setattr(cls, "__factory_fields__", fields)
            cls.__del_fields(cls, fields)
            cls.__instance = super().__new__(cls)
        cls.__new__ = lambda _: cls.__instance
        return cls.__instance

    def __del_fields(cls, fields):
        for key in fields:
            delattr(cls, key)

    def __init__(self) -> None:
        pass

    def digest(self, params: dict = None) -> None:
        """Consumes dictionary of values and returns SimpleNamespace
        containing cleaned values of fields. Redundant params will be
        ignored. If a value is missing, None will be passed to coresponding
        field.

        :param params: dictionary of values, defaults to None
        :type params: dict, optional
        :return: namespace with cleaned values.
        :rtype: SimpleNamespace
        """
        namespace = SimpleNamespace()
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            cleaned_value = field.digest(param_value)
            setattr(namespace, name, cleaned_value)
        return namespace

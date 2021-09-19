# -*- coding: utf-8 -*-
from __future__ import annotations
from types import SimpleNamespace
from PyR3.factory.MeshFactory import MeshFactory, getfields
from .FieldABC import Field


class Struct(Field):

    __instance: Struct = None

    def __new__(cls: Struct) -> Struct:
        if cls.__instance is None:
            fields = MeshFactory.get_field_names(cls.__qualname__, cls.__dict__)
            setattr(cls, "$fields", fields)
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
        namespace = SimpleNamespace()
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            cleaned_value = field.digest(param_value)
            setattr(namespace, name, cleaned_value)
        return namespace

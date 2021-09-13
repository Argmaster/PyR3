# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABCMeta, abstractmethod, abstractproperty
from inspect import isclass
from operator import getitem
from PyR3.factory.fields.FieldABC import Field
from PyR3.factory.fields.Unit import Length
from typing import List, Tuple, Type


class MeshFactoryMeta(ABCMeta):

    required_members = [
        ["__doc__", lambda v: isinstance(v, str)],
        ["__author__", lambda v: isinstance(v, str)],
        ["__version__", lambda v: (isinstance(v, list) and 3 <= len(v) <= 4)],
    ]

    def __new__(cls, name, bases, attributes) -> None:
        cls.check_has_members(name, attributes)
        attributes["$fields"] = cls.get_field_names(attributes)
        attributes["$fields"] |= cls.get_inherited_fields(bases)
        return ABCMeta.__new__(cls, name, bases, attributes)

    def get_field_names(attributes: dict) -> dict:
        fields = {}
        for name, field in attributes.items():
            if isclass(field) and issubclass(field, Field):
                fields[name] = field
        return fields

    def get_inherited_fields(bases: Tuple[Type[MeshFactory]]) -> dict:
        inherited_fields = {}
        for base in bases:
            if issubclass(base, MeshFactory):
                inherited_fields.update(getfields(base))
        return inherited_fields

    def check_has_members(classname, attributes):
        for name, validator in MeshFactoryMeta.required_members:
            if (value := attributes.get(name, None)) is None:
                raise TypeError(
                    f"Trying to create class {classname} without required member {name}."
                )
            if not validator(value):
                raise TypeError(
                    f"Trying to create class {classname} with {name} of invalid type."
                )


"""for attribute_name in dir(self):
    attribute = getattr(self, attribute_name)
    if isinstance(attribute, Field):
        field_type: Field = attribute
        param_value = params.get(attribute_name)
        field_instance = field_type(param_value)
        setattr(self, attribute_name, field_instance)"""


class MeshFactory(metaclass=MeshFactoryMeta):
    """Base class for all mesh factories.
    Defines interface of a mesh factory.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = [1, 0, 0]

    def __init__(self, params: dict) -> None:
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            if param_value is None:
                raise KeyError(
                    f"Missing Factory Field parameter '{name}' for factory {self.__class__.__qualname__}."
                )
            cleaned_value = field(param_value).get()
            setattr(self, name, cleaned_value)


    @abstractmethod
    def render(self):
        pass


def getfields(mesh_factory: MeshFactory) -> dict:
    """Returns fields specified for given MeshFactory.

    :param mesh_factory: Object to fetch fields from.
    :type mesh_factory: MeshFactory
    :return: dictionary of factory fields.
    :rtype: dict
    """
    if isclass(mesh_factory):
        return mesh_factory.__dict__["$fields"]
    else:
        return mesh_factory.__class__.__dict__["$fields"]

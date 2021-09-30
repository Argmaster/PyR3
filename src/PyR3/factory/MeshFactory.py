# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from inspect import isclass
from typing import Tuple
from typing import Type

import bpy

from PyR3.factory.fields.Field import Field
from PyR3.shortcut.context import Objects
from PyR3.shortcut.context import temporary_scene


class _MeshFactoryMeta(ABCMeta):

    required_members = [
        ["__doc__", lambda v: isinstance(v, str)],
        ["__author__", lambda v: isinstance(v, str)],
        ["__version__", lambda v: isinstance(v, str)],
    ]

    def __new__(cls, name, bases, attributes) -> None:
        cls.check_has_members(name, attributes)
        attributes["__factory_fields__"] = cls.get_field_names(cls, name, attributes)
        attributes["__factory_fields__"] |= cls.get_inherited_fields(bases)
        instance = ABCMeta.__new__(cls, name, bases, attributes)
        cls.wrap_render(instance)
        return instance

    def get_field_names(cls, classname, attributes: dict) -> dict:
        fields = {}
        for name, field in attributes.items():
            if isinstance(field, Field):
                field._set_trace_info(name, classname)
                fields[name] = field
            elif isclass(field) and issubclass(field, Field):
                field = field()
                field._set_trace_info(name, classname)
                fields[name] = field
        return fields

    def get_inherited_fields(bases: Tuple[Type[MeshFactory]]) -> dict:
        inherited_fields = {}
        for base in bases:
            if issubclass(base, MeshFactory):
                inherited_fields.update(getfields(base))
        return inherited_fields

    @classmethod
    def check_has_members(cls, classname, attributes):
        for name, validator in cls.required_members:
            if (value := attributes.get(name, None)) is None:
                raise TypeError(
                    f"Trying to create class {classname} without required member {name}."
                )
            if not validator(value):
                raise TypeError(
                    f"Trying to create class {classname} with {name} of invalid type."
                )

    @classmethod
    def wrap_render(cls, instance: MeshFactory):
        old_render = instance.render

        def render(*args, **kwargs):
            with temporary_scene():
                old_render(*args, **kwargs)

        instance.render = render


class MeshFactory(metaclass=_MeshFactoryMeta):
    """
    Base class for a mesh factory object.
    Mesh factory requires __doc__, __author__ and __version__ to be defined
    in mesh factory subclass, otherwise class instantiation will fail.
    Mesh factory can (and should) make use of Fields (subclasses of Field class)
    to specify mesh factory customization params. See PyR3.factory.fields modules
    for first-party fields. To specify field just set class attribute to instance of
    Field subclass.
    See :doc:`MeshFactory usage <../usage/factory>`.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "2.0.0"

    def __init__(self, params: dict) -> None:
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            cleaned_value = field.digest(param_value)
            setattr(self, name, cleaned_value)

    @abstractmethod
    def render(self):
        """Implements rendering process. You can access cleaned contents
        of fields via self.field_name. Rendering process shouldn't alter
        scenes, as it's always happening in isolated scene.
        Only things that are selected when this function returns will
        be copied into callers scene.
        """


def getfields(mesh_factory: MeshFactory) -> dict:
    """Returns fields specified for given MeshFactory.

    :param mesh_factory: Object to fetch fields from.
    :type mesh_factory: MeshFactory
    :return: dictionary of factory fields.
    :rtype: dict
    """
    if isclass(mesh_factory):
        return mesh_factory.__dict__["__factory_fields__"]
    else:
        return mesh_factory.__class__.__dict__["__factory_fields__"]

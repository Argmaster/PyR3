# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABCMeta, abstractmethod, abstractproperty
from contextlib import contextmanager
from inspect import isclass

import bpy
from PyR3.factory.fields.FieldABC import Field
from PyR3.shortcut.context import Objects, delScene, getScene, newScene, setScene
from typing import Tuple, Type


class MeshFactoryMeta(ABCMeta):

    required_members = [
        ["__doc__", lambda v: isinstance(v, str)],
        ["__author__", lambda v: isinstance(v, str)],
        ["__version__", lambda v: (isinstance(v, list) and 3 <= len(v) <= 4)],
    ]

    def __new__(cls, name, bases, attributes) -> None:
        cls.check_has_members(name, attributes)
        attributes["$fields"] = cls.get_field_names(cls, name, attributes)
        attributes["$fields"] |= cls.get_inherited_fields(bases)
        instance = ABCMeta.__new__(cls, name, bases, attributes)
        cls.wrap_render(instance)
        return instance

    def get_field_names(cls, classname, attributes: dict) -> dict:
        fields = {}
        for name, field in attributes.items():
            if isinstance(field, Field):
                field.set_trace_info(name, classname)
                fields[name] = field
            elif isclass(field) and issubclass(field, Field):
                field = field()
                field.set_trace_info(name, classname)
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
            with cls.use_new_scene() as (new, old):
                old_render(*args, **kwargs)
                cls.move_selected_to_old(new, old)

        instance.render = render

    @contextmanager
    def use_new_scene() -> Tuple[bpy.types.Scene, bpy.types.Scene]:
        old_scene = getScene()
        newScene()
        yield getScene(), old_scene
        # clean-up code here
        delScene()
        setScene(old_scene)

    def move_selected_to_old(new: bpy.types.Scene, old: bpy.types.Scene):
        for selected in Objects.selected:
            old.collection.objects.link(selected)
        for selected in Objects.selected:
            new.collection.objects.unlink(selected)


class MeshFactory(metaclass=MeshFactoryMeta):
    """Base class for all mesh factories.
    Defines interface of a mesh factory.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = [1, 0, 0]

    def __init__(self, params: dict) -> None:
        for name, field in getfields(self).items():
            param_value = params.get(name, None)
            cleaned_value = field.digest(param_value)
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

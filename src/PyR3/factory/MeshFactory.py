# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib
from abc import ABCMeta, abstractmethod
from inspect import isclass
from typing import Dict, Mapping, Tuple, Type

from PyR3.factory.fields.Field import Field
from PyR3.shortcut.context import Objects, temporary_scene


class _MeshFactoryMeta(ABCMeta):

    required_members = [
        ["__doc__", lambda v: isinstance(v, str)],
        ["__author__", lambda v: isinstance(v, str)],
        ["__version__", lambda v: isinstance(v, str)],
    ]

    def __new__(
        cls,
        MF_name: str,
        MF_base_classes: Tuple[type],
        attributes: Dict[str, Field],
    ) -> None:
        cls.check_for_required_members(MF_name, attributes)
        attributes["__factory_fields__"] = cls.get_custom_fields_dict(
            cls, MF_name, attributes
        )
        attributes["__factory_fields__"].update(
            cls.get_inherited_fields_list(MF_base_classes)
        )
        instance = ABCMeta.__new__(cls, MF_name, MF_base_classes, attributes)
        cls.assign_wrapped_render(instance)
        return instance

    def get_custom_fields_dict(cls, classname: str, attributes: dict) -> dict:
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

    def get_inherited_fields_list(bases: Tuple[Type[MeshFactory]]) -> dict:
        inherited_fields = {}
        for base in bases:
            if issubclass(base, MeshFactory):
                inherited_fields.update(getfields(base))
        return inherited_fields

    @classmethod
    def check_for_required_members(cls, classname, attributes):
        """Checks if subclass of MeshFactory has set required members, then
        calls custom validators on them,"""
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
    def assign_wrapped_render(cls, instance: MeshFactory):
        custom_render_method = instance.render

        def render_call_wrapper(*args, **kwargs):
            self = args[0]
            with temporary_scene():
                custom_render_method(*args, **kwargs)
                # override $autoselect in render to change this behavior
                if getattr(self, "$autoselect", True):
                    Objects.select_all()

        setattr(instance, "render", render_call_wrapper)


class MeshFactory(metaclass=_MeshFactoryMeta):
    """Base class for a mesh factory object.

    Mesh factory requires __doc__, __author__ and __version__ to be
    defined in mesh factory subclass, otherwise class instantiation will
    fail. Mesh factory can (and should) make use of Fields (subclasses
    of Field class) to specify mesh factory customization params. See
    PyR3.factory.fields modules for first-party fields. To specify field
    just set class attribute to instance of Field subclass. See
    :doc:`MeshFactory usage <../usage/factory>`.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "2.0.0"

    def __init__(self, **MF_params) -> None:
        for name, field in getfields(self).items():
            param_value = MF_params.get(name, None)
            cleaned_value = field.digest(param_value)
            setattr(self, name, cleaned_value)

    @abstractmethod
    def render(self):
        """Implements rendering process.

        You can access cleaned contents of fields via self.field_name.
        Rendering process shouldn't alter scenes, as it's always
        happening in isolated scene. Only things that are selected when
        this function returns will be copied into callers scene.
        """

    @staticmethod
    def build_external(class_: str | MeshFactory, **params) -> Objects:
        if isinstance(class_, str):
            class_ = import_factory(class_)
        class_(**params).render()
        return Objects.selected

    @staticmethod
    def build_external_direct_map(
        class_: str | MeshFactory, param_source: Mapping
    ) -> Objects:
        if isinstance(class_, str):
            class_ = import_factory(class_)
        params = {}
        for field_name in getfields(class_).keys():
            params[field_name] = getattr(param_source, field_name)
        class_(**params).render()
        return Objects.selected

    def prevent_autoselect(self):
        setattr(self, "$autoselect", False)


def getfields(mesh_factory: MeshFactory) -> Dict[str, Field]:
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


def import_factory(class_: str):
    """Imports factory class from module.

    :param class_: python import name in form <python_module_import_path>.class
    :type class_: str
    :raises TypeError: Raised if requested class is not descendant of MeshFactory.
    """
    module_name, class_name = class_.rsplit(".", 1)
    module = importlib.import_module(module_name)
    class_object = getattr(module, class_name)
    if not issubclass(class_object, MeshFactory):
        raise TypeError(
            f"Requested class '{class_name}' is not a MeshFactory."
        )
    return class_object

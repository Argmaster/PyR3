# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List

import bpy


Object = bpy.types.Object


class _ContextMeta(type):
    @property
    def active(cls) -> Object:
        return bpy.context.active_object

    @active.setter
    def active(cls, object_: Object):
        bpy.context.view_layer.objects.active = object_

    @property
    def selected(cls) -> List[Object]:
        return bpy.context.selected_objects


class Context(metaclass=_ContextMeta):

    """
    Provides context altering functionalities, grouped in one place.
    """

    #: Currently active object. It can be set to change active object.
    active: Object
    #: List of currently selected objects.
    #: This property is read-only.
    #: Use methods to alter selection.
    selected: List[Object]

    @staticmethod
    def select(*ob: Object):
        """Select given object(s).

        :param ob: object(s) to select
        :type ob: Object
        """
        for ob_ in ob:
            ob_.select_set(True)

    @staticmethod
    def deselect(*ob: Object):
        """Deselect given object(s).

        :param ob: object(s) to deselect
        :type ob: Object
        """
        for ob_ in ob:
            ob_.select_set(True)

    @staticmethod
    def selectAll():
        """Selects all objects available in viewport."""
        bpy.ops.object.select_all(action="SELECT")

    @staticmethod
    def deselectAll():
        """Deselects all objects available in viewport."""
        bpy.ops.object.select_all(action="DESELECT")

    @classmethod
    def selectOnly(cls, *ob: Object):
        """Deselects all objects and selects only given one(s).

        :param ob: Object(s) to select
        :type ob: Object
        """
        cls.deselectAll()
        cls.select(*ob)


if __name__ == "__main__":
    pass

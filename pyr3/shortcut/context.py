# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List
from collections import UserList

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
    def selected(cls) -> Objects[Object]:
        return Objects(bpy.context.selected_objects)


class Objects(list, metaclass=_ContextMeta):

    """
    As a class, provides set of static functionalities for managing global
    selection and currently selected and active objects.

    As a instance, is a container for objects with possibility to select
    or deselect object(s) contained inside.
    """

    #: Currently active object. It can be set to change active object.
    active: Object
    #: List of currently selected objects.
    #: This property is read-only.
    #: Use methods to alter selection.
    selected: Objects[Object]

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

    @classmethod
    def delete(cls, *ob: Object) -> None:
        """Delete object(s) ob. It keeps previously selected object(s) selected.

        :param ob: Object(s) to select
        :type ob: Object
        """
        cls.deselect(*ob)
        with TemporarilySelected(*ob):
            bpy.ops.object.delete()

    @classmethod
    def deleteAll(cls) -> None:
        """Deletes all selectable objects."""
        cls.selectAll()
        bpy.ops.object.delete()

    @classmethod
    def duplicate(cls, *ob: Object) -> None:
        """Duplicates object(s)

        :param ob: object(s) to duplicate
        :type ob: Object
        """
        with TemporarilySelected(*ob):
            bpy.ops.object.duplicate()

    def selectContained(self):
        """Selects elements contained in this sequence."""
        self.select(*self)

    def deselectContained(self):
        """Deselects elements contained in this sequence."""
        self.deselect(*self)

    def selectOnlyContained(self):
        """Selects only elements contained in this sequence."""
        self.selectOnly(*self)

    def only(self) -> Object:
        """Returns only element in sequence.

        :raises ValueError: If sequence is empty or has more than one element.
        :return: Only element from sequence
        :rtype: Object
        """
        if len(self) == 1:
            return self[0]
        else:
            raise ValueError("Objects list doesn't contain one element.")

    def __str__(self) -> str:
        return f"Objects{super().__str__()}"


class TemporarilySelected:
    """For context manager usage, on enter selects only objects
    passed to constructor, on exit restores selection on previously selected objects.
    """

    def __init__(self, *ob: Object) -> None:
        self.ob = ob

    def __enter__(self):
        self.previously_selected = Objects.selected
        Objects.selectOnly(*self.ob)

    def __exit__(self, type, value, traceback):
        Objects.selectOnly(*self.previously_selected)


def getScene() -> bpy.types.Scene:
    """Returns currently used scene.

    :return: Scene
    :rtype: bpy.types.Scene
    """
    return bpy.context.window.scene


def setScene(scene: bpy.types.Scene) -> None:
    """Sets new scene to use.

    :param scene: Scene
    :type scene: bpy.types.Scene
    """
    bpy.context.window.scene = scene


def newScene() -> None:
    """Creates new Scene object and automatically
    sets it as currently used one.
    """
    bpy.ops.scene.new()


def delScene() -> None:
    """Deletes currently used scene.
    """
    bpy.ops.scene.delete()


if __name__ == "__main__":
    print(Objects.selected)

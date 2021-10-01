# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import UserList
from contextlib import contextmanager
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
            ob_.select_set(False)

    @staticmethod
    def select_all():
        """Selects all objects available in viewport."""
        bpy.ops.object.select_all(action="SELECT")

    @staticmethod
    def deselect_all():
        """Deselects all objects available in viewport."""
        bpy.ops.object.select_all(action="DESELECT")

    @classmethod
    def select_only(cls, *ob: Object):
        """Deselects all objects and selects only given one(s).

        :param ob: Object(s) to select
        :type ob: Object
        """
        cls.deselect_all()
        cls.select(*ob)

    @classmethod
    def delete(cls, *ob: Object) -> None:
        """Delete object(s) ob. It keeps previously selected object(s) selected.

        :param ob: Object(s) to select
        :type ob: Object
        """
        cls.deselect(*ob)
        with temporarily_selected(*ob):
            bpy.ops.object.delete()

    @classmethod
    def delete_all(cls) -> None:
        """Deletes all selectable objects."""
        cls.select_all()
        bpy.ops.object.delete()

    @classmethod
    def duplicate(cls, *ob: Object) -> None:
        """Duplicates object(s)

        :param ob: object(s) to duplicate
        :type ob: Object
        """
        with temporarily_selected(*ob):
            bpy.ops.object.duplicate()

    @staticmethod
    def inverse_selection():
        bpy.ops.object.select_all(action="INVERT")

    def select_contained(self):
        """Selects elements contained in this sequence."""
        self.select(*self)

    def deselect_contained(self):
        """Deselects elements contained in this sequence."""
        self.deselect(*self)

    def select_only_contained(self):
        """Selects only elements contained in this sequence."""
        self.select_only(*self)

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

    @staticmethod
    def all():
        return Objects(bpy.context.scene.objects)


@contextmanager
def temporarily_selected(*ob: Object):
    """For context manager usage, on enter selects only objects
    passed to constructor, on exit restores selection on previously selected objects.
    """
    # preparation
    previously_selected = Objects.selected
    Objects.select_only(*ob)
    # yield execution to caller
    yield
    # back here for clean-up
    Objects.select_only(*previously_selected)


@contextmanager
def temporary_scene():
    """Creates temporary scene and sets it as currently used.
    After exit, all objects selected in temporary scene are
    copied into previous scene and previous scene is set as
    currently used.

    :yield: (new, old) scenes
    :rtype: Tuple[bpy.types.Scene, bpy.types.Scene]
    """
    # preperation
    old = getScene()
    newScene()
    new = getScene()
    # yield execution to caller
    yield new, old
    # clean-up code here
    for selected in Objects.selected:
        old.collection.objects.link(selected)
    for selected in Objects.selected:
        new.collection.objects.unlink(selected)
    delScene()


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
    sets it as currently used one."""
    bpy.ops.scene.new()


def delScene() -> None:
    """Deletes currently used scene."""
    bpy.ops.scene.delete()


def cleanScene() -> None:
    """Deletes current scene and creates new one.
    Be aware that for total clean-up you should call
    wipeScenes() instead, as it destroys **ALL** scenes,
    not only current one, as cleanScene() does.
    """
    old_scene = getScene()
    newScene()
    new_scene = getScene()
    setScene(old_scene)
    delScene()
    setScene(new_scene)


def listScenes() -> List[bpy.types.Scene]:
    """Returns list of existing scenes."""
    return list(bpy.data.scenes)


def wipeScenes() -> None:
    """Destroys all existing ones and creates new empty one."""
    for _ in listScenes()[:-1]:
        delScene()
    cleanScene()

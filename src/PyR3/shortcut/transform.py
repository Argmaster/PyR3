# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import bpy

from .context import Objects, temporarily_selected


class ApplyProxyObject:
    _target_objects: Objects

    def __init__(self, ob: Objects) -> None:
        self._target_objects = ob

    def apply_transform(self):
        with temporarily_selected(*self._target_objects):
            bpy.ops.object.transform_apply(
                location=True, rotation=False, scale=False
            )

    def apply_rotation(self):
        with temporarily_selected(*self._target_objects):
            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False
            )

    def apply_scale(self):
        with temporarily_selected(*self._target_objects):
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True
            )

    def apply_all(self):
        with temporarily_selected(*self._target_objects):
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True
            )


def move(
    vector: Tuple[float, float, float],
    **kwargs,
) -> ApplyProxyObject:
    """Move selected objects.

    :param vector: absolute coordinates to move to
    :type vector: Tuple[float, float, float], optional
    :param `**kwargs`: All from `bpy.ops.transform.translate <https://docs.blender.org/api/current/bpy.ops.transform.html#bpy.ops.transform.translate>`_.
    """
    bpy.ops.transform.translate(
        value=vector,
        **kwargs,
    )
    return ApplyProxyObject(Objects.selected)


def rotate(
    angle: float,
    orient_axis: str,
    **kwargs,
) -> ApplyProxyObject:
    """Rotate selected objects around `orient_axis`

    :param angle: rotation angle
    :type angle: float, optional
    :param orient_axis: axis to rotate around, either "X", "Y" or "Z".
    :type orient_axis: str, optional
    :param `**kwargs`: All from `bpy.ops.transform.rotate <https://docs.blender.org/api/current/bpy.ops.transform.html#bpy.ops.transform.rotate>`_.
    """
    context_override = bpy.context.copy()
    context_override["area"] = [
        a for a in bpy.context.screen.areas if a.type == "VIEW_3D"
    ][0]
    bpy.ops.transform.rotate(
        context_override,
        value=angle,
        orient_axis=orient_axis,
        **kwargs,
    )
    return ApplyProxyObject(Objects.selected)


def scale(
    scales: Tuple[float, float, float],
    **kwargs,
):
    """Scale (resize) selected objects.

    :param scales: Tuple of scales for each axis, (x, y, z)
    :type scales: tuple, optional
    :param `**kwargs`: All from `bpy.ops.transform.resize <https://docs.blender.org/api/current/bpy.ops.transform.html#bpy.ops.transform.resize>`_.
    """
    bpy.ops.transform.resize(
        value=scales,
        **kwargs,
    )
    return ApplyProxyObject(Objects.selected)


class Transform:

    """This class is a container for set of object transforming functions.

    They all operate on global (currently selected) object(s).
    """

    @staticmethod
    def apply(
        do_move: bool = False,
        do_rotation: bool = False,
        do_scale: bool = False,
    ):
        """Apply the object's transformation to its data.

        :param use_move: applies move if true, defaults to False
        :type use_move: bool, optional
        :param use_rotation: applies rotation if true, defaults to False
        :type use_rotation: bool, optional
        :param use_scale: applies scale if true, defaults to False
        :type use_scale: bool, optional
        """
        print(
            "PyR3.shortcut.transform.Transform.apply() is deprecated, "
            "use ApplyProxyObject object returned "
            "from transformation functions instead."
        )
        bpy.ops.object.transform_apply(
            location=bool(do_move),
            rotation=bool(do_rotation),
            scale=bool(do_scale),
        )

    @staticmethod
    def move(*args, **kwargs):
        print(
            "PyR3.shortcut.transform.Transform.move() is deprecated"
            "PyR3.shortcut.transform.move() function instead."
        )
        return move(*args, **kwargs)

    @staticmethod
    def rotate(*args, **kwargs):
        print(
            "PyR3.shortcut.transform.Transform.rotate() is deprecated"
            "PyR3.shortcut.transform.rotate() function instead."
        )
        return rotate(*args, **kwargs)

    @staticmethod
    def scale(*args, **kwargs):
        print(
            "PyR3.shortcut.transform.Transform.scale() is deprecated"
            "PyR3.shortcut.transform.scale() function instead."
        )
        return scale(*args, **kwargs)

    @staticmethod
    def resize(*args, **kwargs):
        print(
            "PyR3.shortcut.transform.Transform.resize() is deprecated"
            "PyR3.shortcut.transform.scale() function instead."
        )
        return scale(*args, **kwargs)

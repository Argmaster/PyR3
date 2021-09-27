# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import bpy


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
        bpy.ops.object.transform_apply(
            location=do_move, rotation=do_rotation, scale=do_scale
        )

    @classmethod
    def move(
        cls,
        vector: Tuple[float, float, float],
        **kwargs,
    ):
        """Move selected objects.

        :param vector: absolute coordinates to move to
        :type vector: Tuple[float, float, float], optional
        :param `**kwargs`: All from `bpy.ops.transform.translate <https://docs.blender.org/api/current/bpy.ops.transform.html#bpy.ops.transform.translate>`_.
        """
        bpy.ops.transform.translate(
            value=vector,
            **kwargs,
        )

    @classmethod
    def rotate(
        cls,
        angle: float,
        orient_axis: str,
        **kwargs,
    ):
        """Rotate selected objects around `orient_axis`

        :param angle: rotation angle
        :type angle: float, optional
        :param orient_axis: axis to rotate around, either "X", "Y" or "Z".
        :type orient_axis: str, optional
        :param `**kwargs`: All from `bpy.ops.transform.rotate <https://docs.blender.org/api/current/bpy.ops.transform.html#bpy.ops.transform.rotate>`_.
        """
        bpy.ops.transform.rotate(
            angle=angle,
            orient_axis=orient_axis,
            **kwargs,
        )

    @classmethod
    def scale(
        cls,
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

    resize = scale

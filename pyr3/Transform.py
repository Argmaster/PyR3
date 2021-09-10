# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import bpy


class Transform:

    """This class is a container for set of object transforming functions. They all operate on global object,
    therefore they are all static. Each of transformation methods can be given a `orient_type` param, to select
    desired orientation. Possible transformation orient types are:

    - GLOBAL , Align the transformation axes to world space.

    - LOCAL , Align the transformation axes to the selected objects' local space.

    - NORMAL , Align the transformation axes to average normal of selected elements (bone Y axis for pose mode).

    - GIMBAL , Align each axis to the Euler rotation axis as used for input.

    - VIEW , Align the transformation axes to the window.

    - CURSOR , Align the transformation axes to the 3D cursor.
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

    @staticmethod
    def move(
        vector: Tuple[float, float, float],
        apply: bool = True,
        **kwargs,
    ):
        """Move selected items

        :param vector: absolute coordinates to move to
        :type vector: Tuple[float, float, float], optional
        :param apply: automatically applies transformation if true. See Transform.apply()
        :type bool: Tuple[float, float, float], optional
        :param `**kwargs`: Additional arguments for transformation.
        """
        bpy.ops.transform.translate(
            value=vector,
            **kwargs,
        )
        if apply:
            Transform.apply(True, False, False)

    @staticmethod
    def rotate(
        angle: float,
        orient_axis: str,
        center_override=(0.0, 0.0, 0.0),
        apply: bool = True,
        **kwargs,
    ):
        """Rotate selected objects.

        :param angle: rotation angle
        :type angle: float, optional
        :param orient_axis: axis to rotate around
        :type orient_axis: str, optional
        :param center_override: overrides center of rotation, defaults to (0.0, 0.0, 0.0)
        :type center_override: tuple, optional
        :param apply: automatically applies transformation if true. See Transform.apply()
        :type bool: Tuple[float, float, float], optional
        :param `**kwargs`: Additional arguments for transformation.
        """
        bpy.ops.transform.rotate(
            angle=angle,
            orient_axis=orient_axis,
            center_override=center_override,
            **kwargs,
        )
        if apply:
            Transform.apply(False, True, False)

    @staticmethod
    def scale(
        scales: tuple = (1, 1, 1),
        apply: bool = True,
        **kwargs,
    ):
        """Scale (resize) selected items

        :param scales: scale for each axis, defaults to (1, 1, 1)
        :type scales: tuple, optional
        :param apply: automatically applies transformation if true. See :meth:`PyR3.Transform.apply`
        :type apply: bool, optional
        :param `**kwargs`: Additional arguments for transformation.
        """
        bpy.ops.transform.resize(
            value=scales,
            **kwargs,
        )
        if apply:
            Transform.apply(False, False, True)

    resize = scale

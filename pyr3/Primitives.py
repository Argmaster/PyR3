# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy


class Primitives:
    def addPlane(side_length: float = 1.0):
        """Creates new Plane object at (0, 0, 0).
        It is both active and selected.

        :param side_length: the length of the side of the plane, defaults to 1.0
        :type side_length: float, optional
        """
        bpy.ops.mesh.primitive_plane_add(
            size=side_length, enter_editmode=False
        )

    def addCube(side_length: float = 1.0):
        """Creates new Cube object at (0, 0, 0)

        :param side_length: the length of the side of the cube, defaults to 1.0
        :type side_length: float, optional
        """
        bpy.ops.mesh.primitive_cube_add(
            size=side_length, enter_editmode=False
        )

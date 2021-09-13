"""
Mesh operation shortcuts, including creation, bounding box calculations and more.
"""


# -*- coding: utf-8 -*-
from __future__ import annotations
import bpy

from bpy.types import Object
from mathutils import Vector
from PyR3.shortcut.context import Objects


def boundingBoxCenterPoint(ob: Object) -> Vector:
    """Calculates center of bounding box.

    :param ob: Object to calculate for.
    :type ob: Object
    :return: Center point.
    :rtype: Vector
    """
    local_bbox_center = 0.125 * sum((Vector(b) for b in ob.bound_box), Vector())
    global_bbox_center = ob.matrix_world @ local_bbox_center
    return global_bbox_center


def containingSphereRadius(ob: Object, center: Vector = None) -> float:
    """Calculate radius of a sphere that bounding box can fit in.

    :param ob: Object to calculate for
    :type ob: Object
    :param center: Changes center from bbox center, defaults to None
    :type center: Vector, optional
    :return: radius
    :rtype: float
    """
    if center is None:
        loc = Object.bboxCenter(ob)

    vector_max: Vector = max(
        [(ob.matrix_world @ Vector(bound)) - loc for bound in ob.bound_box]
    )
    return vector_max.length


def boundingBoxPoints(ob: Object) -> float:
    """Calculates object's bounding box

    :param bpy_obj: Object to get bbox of.
    :type bpy_obj: Object
    :return: List of bounding box points.
    :rtype: float
    """
    return [ob.matrix_world @ Vector(b) for b in ob.bound_box]


def convert(ob: Object, target: str = "MESH"):
    """Convert object from one type to another.

    :param ob: Object to transform
    :type ob: Object
    :param target: target object type, defaults to "MESH"
    :type target: str, optional
    """
    Objects.active = ob
    Objects.selectOnly(ob)
    bpy.ops.object.convert(target=target)


def join(*ob: Object):
    """Joins passed objects into one at first object.

    :param ob: Objects to join
    :type ob: Object
    """
    if len(ob) < 2:
        return
    Objects.deselectAll()
    Objects.active = ob[0]
    Objects.select(*ob)
    bpy.ops.object.join()

"""Mesh operation shortcuts, including creation, bounding box calculations and more.
"""
# -*- coding: utf-8 -*-
from __future__ import annotations

import time
from typing import List
from typing import Tuple

import bpy
from bpy.ops import mesh
from bpy.types import Object
from mathutils import Vector

from PyR3.shortcut.context import Objects
from PyR3.shortcut.context import getScene


def __return_active(function):
    def call_and_return_active(*args, **kwargs):
        function(*args, **kwargs)
        return Objects.active

    return call_and_return_active


#: Shortcut for creating circle. It returns created object.
addCircle: mesh.primitive_circle_add = __return_active(mesh.primitive_circle_add)
#: Shortcut for creating cone. It returns created object.
addCone: mesh.primitive_cone_add = __return_active(mesh.primitive_cone_add)
#: Shortcut for creating uv sphere. It returns created object.
addUVSphere: mesh.primitive_uv_sphere_add = __return_active(
    mesh.primitive_uv_sphere_add
)
#: Shortcut for creating cube. It returns created object.
addCube: mesh.primitive_cube_add = __return_active(mesh.primitive_cube_add)
#: Shortcut for creating cylinder. It returns created object.
addCylinder: mesh.primitive_cylinder_add = __return_active(mesh.primitive_cylinder_add)
#: Shortcut for creating grid. It returns created object.
addGrid: mesh.primitive_grid_add = __return_active(mesh.primitive_grid_add)
#: Shortcut for creating ico sphere. It returns created object.
addIcoSphere: mesh.primitive_ico_sphere_add = __return_active(
    mesh.primitive_ico_sphere_add
)
#: Shortcut for creating plane. It returns created object.
addPlane: mesh.primitive_plane_add = __return_active(mesh.primitive_plane_add)
#: Shortcut for creating torus. It returns created object.
addTorus: mesh.primitive_torus_add = __return_active(mesh.primitive_torus_add)


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
    Objects.select_only(ob)
    bpy.ops.object.convert(target=target)


def join(target: Object, *rest: Object):
    """Joins rest objects into target object.
    This will result in merging meshes into one
    object's data.

    :param target: object to join rest into
    :type target: Object
    :param rest: other objects to join
    :type rest: Object
    """
    Objects.deselect_all()
    Objects.active = target
    Objects.select_only(target)
    Objects.select(*rest)
    bpy.ops.object.join()


def fromPyData(
    vertexData: List[Tuple[float, float, float]] = [],
    edgeData: List[Tuple[float, float]] = [],
    faceData: List[Tuple[float, ...]] = [],
    *,
    mesh_name="mesh",
    object_name="object",
) -> Object:
    """Creates new mesh object from python data.

    :param vertexData: list of vertices, defaults to []
    :type vertexData: List[Tuple[float, float, float]], optional
    :param edgeData: list of tuples of edges vertices indexes, defaults to []
    :type edgeData: List[Tuple[float, float]], optional
    :param faceData: list of tuples of faces edge indexes, defaults to []
    :type faceData: List[Tuple[float, ...]], optional
    :param mesh_name: name for mesh data object, defaults to "mesh"
    :type mesh_name: str, optional
    :param object_name: name for mesh object, defaults to "object"
    :type object_name: str, optional
    :return: created object.
    :rtype: Object
    """
    new_mesh = bpy.data.meshes.new(mesh_name)
    new_mesh.from_pydata(vertexData, edgeData, faceData)
    new_mesh.update()
    obj = bpy.data.objects.new(object_name, new_mesh)
    # getScene()
    bpy.context.scene.collection.objects.link(obj)
    return obj

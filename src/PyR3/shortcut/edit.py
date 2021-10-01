# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Callable
from typing import Iterable
from typing import List
from typing import Tuple

import bmesh
import bpy
from bmesh.types import BMEdge
from bmesh.types import BMFace
from bmesh.types import BMVert
from mathutils import Vector

from PyR3.shortcut.context import Objects


class OperationCancelled(Exception):
    pass


def manual_set_edit_mode():
    bpy.ops.object.mode_set(mode="EDIT")


def manual_set_object_mode():
    bpy.ops.object.mode_set(mode="OBJECT")


class Edit:
    """class for automatic in-out switching Edit mode.
    It is meant to be used as context manager with edited
    object being passed as param to constructor.
    """

    _is_edit_mode: bool = False
    BMESH: bmesh.bmesh.types.BMesh = None
    ob: bpy.types.Object

    class MeshCompList(list):
        def selected(self) -> Edit.MeshCompList:
            return Edit.MeshCompList(element for element in self if element.select)

    def __init__(
        self,
        ob: bpy.types.Object,
        *more: bpy.types.Object,
        active: bpy.types.Object = None
    ) -> None:
        self.ob = ob
        self.active = active
        self.more = more

    @staticmethod
    def isEditMode():
        return bpy.context.object.mode == "EDIT"

    def __enter__(self) -> Edit:
        """Enters edit mode, selects everything in there."""
        if self.active is None:
            Objects.active = self.ob
        else:
            Objects.active = self.active
        Objects.select_only(self.ob)
        Objects.select(*self.more)
        manual_set_edit_mode()
        Edit._is_edit_mode = True
        self.BMESH = bmesh.from_edit_mesh(self.ob.data)
        self.select_all()
        return self

    def __exit__(self, class_, instance, traceback) -> None:
        """Return to object mode."""
        manual_set_object_mode()
        Edit._is_edit_mode = False

    def faces(self) -> MeshCompList[BMFace]:
        """Provides access to edited object bmesh attribute
        holding reference to list of all faces of edited mesh.

        :return: List of faces.
        :rtype: MeshCompList[BMFace]
        """
        self.BMESH.faces.ensure_lookup_table()
        return Edit.MeshCompList(self.BMESH.faces)

    def edges(self) -> MeshCompList[BMEdge]:
        """Provides access to edited object bmesh attribute
        holding reference to list of all edges of edited mesh.

        :return: List of edges.
        :rtype: MeshCompList[BMEdge]
        """
        self.BMESH.faces.ensure_lookup_table()
        return Edit.MeshCompList(self.BMESH.edges)

    def vertices(self) -> MeshCompList[BMVert]:
        """Access to edited object bmesh vertice table.

        :return: Vertices
        :rtype: MeshCompList[BMVert]
        """
        self.BMESH.verts.ensure_lookup_table()
        return Edit.MeshCompList(self.BMESH.verts)

    def get_selected_vertices(self) -> List[BMVert]:
        return [v for v in self.vertices() if v.select]

    def select_vertices(
        self,
        condition: Callable[[Vector], bool],
    ):
        """Selects vertices, when condition function returns true.

        :param condition: test callable. It will be given vertice coordinate as parameter.
        :type condition: Callable[Vector], bool]
        """
        for v in self.vertices():
            if condition(v.co):
                v.select = True

    def select_edges(
        self,
        condition: Callable[[Vector, Vector], bool],
    ):
        """Selects edges, when condition function returns true.

        :param condition: Test callable. It will be given edge vertice coordinate as parameter.
        :type condition: Callable[[Vector, Vector], bool]
        """
        for e in self.edges():
            if condition(e.verts[0].co, e.verts[1].co):
                e.select = True

    def select_facing(self, direction: Vector) -> Edit:
        if not isinstance(direction, Vector):
            direction = Vector(direction)
        for face in self.faces():
            if face.normal.dot(direction) == 1:
                face.select = True
        return self

    def select_all(self):
        """Selects whole mesh"""
        bpy.ops.mesh.select_all(action="SELECT")

    def deselect_all(self):
        """Deselects whole mesh"""
        bpy.ops.mesh.select_all(action="DESELECT")

    def invert_selection(self):
        """Invertices selection of mesh components."""
        bpy.ops.mesh.select_all(action="INVERT")

    def delete_vertices(self):
        """Delete selected vertices."""
        bpy.ops.mesh.delete(type="VERT")

    def delete_edges(self):
        """Delete selected edges."""
        bpy.ops.mesh.delete(type="EDGE")

    def delete_faces(self):
        """Delete selected faces."""
        bpy.ops.mesh.delete(type="FACE")

    def duplicate(self, mode: int = 1):
        """Duplicate selected."""
        bpy.ops.mesh.duplicate(mode=mode)

    # methods from blender API, moved here for easier access
    bevel = bpy.ops.mesh.bevel
    extrude = bpy.ops.mesh.extrude_region
    extrude_repeat = bpy.ops.mesh.extrude_repeat
    extrude_individual_faces = bpy.ops.mesh.extrude_edges_indiv
    edge_face_add = bpy.ops.mesh.edge_face_add
    collapse = bpy.ops.mesh.edge_collapse
    remove_doubles = bpy.ops.mesh.remove_doubles
    normals_make_consistent = bpy.ops.mesh.normals_make_consistent

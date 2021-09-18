# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Callable, Iterable, Tuple


import bpy
import bmesh
from PyR3.shortcut.context import Objects
from mathutils import Vector


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

    def __init__(self, ob: bpy.types.Object) -> None:
        self.ob = ob

    @staticmethod
    def isEditMode():
        return Edit._is_edit_mode

    def __enter__(self) -> Edit:
        """Enters edit mode, selects everything in there."""
        Objects.select_only(self.ob)
        manual_set_edit_mode()
        Edit._is_edit_mode = True
        self.BMESH = bmesh.from_edit_mesh(self.ob.data)
        self.select_all()
        return self

    def __exit__(self, class_, instance, traceback) -> None:
        """Return to object mode."""
        manual_set_object_mode()
        Edit._is_edit_mode = False

    def faces(self) -> Iterable:
        """Provides access to edited object bmesh attribute
        holding reference to list of all faces of edited mesh.

        Returns:
            Iterable: list of edited object faces.
        """
        self.BMESH.faces.ensure_lookup_table()
        return self.BMESH.faces

    def edges(self) -> Iterable:
        """Provides access to edited object bmesh attribute
        holding reference to list of all edges of edited mesh.

        Returns:
            Iterable: list of edited object edges.
        """
        self.BMESH.faces.ensure_lookup_table()
        return self.BMESH.edges

    def verts(self) -> Iterable:
        """Access to edited object bmesh vertice table.

        :return: Vertices
        :rtype: Iterable
        """
        self.BMESH.verts.ensure_lookup_table()
        return self.BMESH.verts

    def selectVerts(
        self,
        condition: Callable[[Vector], bool],
    ):
        """Selects vertices, when condition function returns true.

        :param condition: test callable. It will be given vertice coordinate as parameter.
        :type condition: Callable[Vector], bool]
        """
        for v in self.verts:
            if condition(v.co):
                v.select = True

    def selectEdges(
        self,
        condition: Callable[[Vector, Vector], bool],
    ):
        """Selects edges, when condition function returns true.

        :param condition: Test callable. It will be given edge vertice coordinate as parameter.
        :type condition: Callable[[Vector, Vector], bool]
        """
        for e in self.edges:
            if condition(e.verts[0].co, e.verts[1].co):
                e.select = True

    def selectFacing(self, direction: Vector) -> Edit:
        for face in self.faces:
            if face.normal.dot(direction) == 1:
                face.select = True
        return self

    def select_all(self):
        """Selects whole mesh"""
        bpy.ops.mesh.select_all(action="SELECT")

    def deselect_all(self):
        """Deselects whole mesh"""
        bpy.ops.mesh.select_all(action="DESELECT")

    # methods from blender API, contained here to make it
    # obvious that they can be used to alter mesh.
    invert_selection = lambda: bpy.ops.mesh.select_all(action="INVERT")
    select_nth = bpy.ops.mesh.select_nth
    select_face_by_sides = bpy.ops.mesh.select_face_by_sides

    delete = bpy.ops.mesh.delete
    duplicate = bpy.ops.mesh.duplicate
    bevel = bpy.ops.mesh.bevel
    extrude = bpy.ops.mesh.extrude_region
    extrude_repeat = bpy.ops.mesh.extrude_repeat
    extrude_individual_faces = bpy.ops.mesh.extrude_edges_indiv
    edge_face_add = bpy.ops.mesh.edge_face_add
    collapse = bpy.ops.mesh.edge_collapse
    remove_doubles = bpy.ops.mesh.remove_doubles
    normals_make_consistent = bpy.ops.mesh.normals_make_consistent

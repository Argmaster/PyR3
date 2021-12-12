# -*- coding: utf-8 -*-
from __future__ import annotations

import math

import numpy

from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Boolean, Integer
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import continuous_edge, fromPyData
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.transform import Transform


class LCurve(MeshFactory):
    """MF capable of generating straight or L like bend shaped (commonly used
    as pins for microchips)."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "1.0.0"

    total_width = Length()
    total_heigh = Length()
    bend = Boolean(default=False)
    bend_radius = Length()
    bend_segments = Integer(value_range=range(4, 128))
    width = Length()
    bevel = Integer(value_range=range(0, 128))
    bevel_depth = Length()
    material = BSDF_Material()

    def render(self) -> None:
        Z_VERTICAL_LIMIT = self.total_heigh - self.bend_radius - self.width
        Z_TOP_LEVEL = self.total_heigh - self.width
        Y_LOCATION = self.width / 2
        vertices = [
            (self.width, Y_LOCATION, 0),
            (self.width, Y_LOCATION, Z_VERTICAL_LIMIT),
            *self.get_arc_verts(Y_LOCATION, Z_VERTICAL_LIMIT),
            (self.total_width, Y_LOCATION, Z_TOP_LEVEL),
        ]
        base_mesh = fromPyData(vertices, continuous_edge(vertices))
        with Edit(base_mesh) as mesh:
            mesh.extrude()
            Transform.move((0, -self.width, 0))
        Solidify(base_mesh, thickness=self.width).apply()

    def get_arc_verts(self, Y_LOCATION: float, Z_BASE_LEVEL: float):

        RADIUS = self.bend_radius

        def x_function(x):
            return RADIUS * math.sin(x)

        def z_function(y):
            return RADIUS * math.cos(y)

        return [
            (
                x_function(a) + self.bend_radius + self.width,
                Y_LOCATION,
                z_function(a) + Z_BASE_LEVEL,
            )
            for a in numpy.linspace(-math.pi / 2, 0, self.bend_segments)[1:]
        ]

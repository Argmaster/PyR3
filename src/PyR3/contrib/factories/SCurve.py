# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy

from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.material import apply_BSDF_material_params
from PyR3.shortcut.mesh import continuous_edge, fromPyData
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.transform import move


class SCurve(MeshFactory):
    """MF capable of generating 'S' like shapes (commonly used as microchip
    pins)."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "1.0.0"

    total_width = Length()
    total_height = Length()
    total_depth = Length()
    lower_length = Length()
    upper_length = Length()
    steps = Integer(value_range=range(4, 128))
    thickness = Length()
    material = BSDF_Material()

    def render(self) -> None:
        HALF_TOTAL_WIDTH: float = self.total_width / 2
        HALF_TOTAL_HEIGHT: float = (self.total_height - self.thickness) / 2
        vertices = self.generate_vertices_list(
            HALF_TOTAL_WIDTH, HALF_TOTAL_HEIGHT
        )
        CURVE_MESH_OB = fromPyData(vertices, continuous_edge(vertices))
        apply_BSDF_material_params(CURVE_MESH_OB, self.material)
        with Edit(CURVE_MESH_OB) as edit:
            move((0, -self.total_depth / 2, 0))
            edit.extrude()
            move((0, self.total_depth, 0))
        # final touches - thickness and volume quality
        Solidify(CURVE_MESH_OB, self.thickness, offset=0).apply()

    def generate_vertices_list(self, half_total_width, half_total_height):
        vertices = [
            (-half_total_width, 0, -half_total_height),
            (-half_total_width + self.lower_length, 0, -half_total_height),
        ]
        curve_vertices = self.generate_curve_points(
            half_total_width, half_total_height
        )
        vertices.extend(curve_vertices)
        # last 2 verts
        vertices.append(
            (half_total_width - self.upper_length, 0, half_total_height)
        )
        vertices.append((half_total_width, 0, half_total_height))
        return vertices

    def generate_curve_points(self, half_total_width, half_total_height):
        vertices = []
        difference = self.total_width - self.lower_length - self.upper_length
        x_step_length = difference / self.steps
        sin_arg_step_length = numpy.pi / self.steps
        for i in range(1, self.steps - 1):
            sin_argument = i * sin_arg_step_length - numpy.pi / 2
            z_value = numpy.sin(sin_argument) * half_total_height
            vertices.append(
                (
                    (i * x_step_length) - half_total_width + self.lower_length,
                    0,
                    z_value,
                )
            )
        return vertices
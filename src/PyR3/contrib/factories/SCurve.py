# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy

from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.context import Objects
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.material import apply_BSDF_material_params
from PyR3.shortcut.mesh import continuous_edge, fromPyData
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.transform import Transform


class SCurve(MeshFactory):
    """Class description."""

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
        half_total_width = self.total_width / 2
        half_total_height = (self.total_height - self.thickness) / 2
        vertices = self.generate_vertices_list(
            half_total_width, half_total_height
        )
        curve_mesh = fromPyData(vertices, continuous_edge(vertices))
        with Edit(curve_mesh) as edit:
            edit.extrude()
            Transform.move((0, self.total_width, 0))
        # final touches - thickness and volume quality
        Solidify(curve_mesh, self.thickness, offset=0).apply()
        apply_BSDF_material_params(Objects.active, self.material)

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

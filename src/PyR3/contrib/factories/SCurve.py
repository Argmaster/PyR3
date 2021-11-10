# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy

from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.edit import Edit
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

    def generate_vertices_list(self, half_total_width, half_total_height):
        lower_limit = -half_total_width + self.lower_length
        upper_limit = half_total_width - self.upper_length
        difference = upper_limit - lower_limit
        vertices = [
            (-half_total_width, 0, -half_total_height),
            (lower_limit, 0, -half_total_height),
        ]
        for step in numpy.linspace(lower_limit, upper_limit, self.steps)[1:-1]:
            normalized = step / difference
            z_value = numpy.sin(normalized * numpy.pi) * half_total_height
            vertices.append((step, 0, z_value))
        # pre-last vert
        vertices.append((upper_limit, 0, half_total_height))
        # last vert
        vertices.append((half_total_width, 0, half_total_height))
        return vertices
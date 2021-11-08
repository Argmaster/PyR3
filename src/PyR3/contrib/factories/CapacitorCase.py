# -*- coding: utf-8 -*-

from PyR3.factory.fields.Number import Float, Integer
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.context import Objects
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import addCircle
from PyR3.shortcut.modifiers import Bevel
from PyR3.shortcut.transform import Transform


class CapacitorCase(MeshFactory):
    """Generates cylindrical meshes looking similar to electrolytic capacitor
    cases."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "0.0.0"

    h1 = Length()
    h2 = Length()
    h3 = Length()
    scale = Float(not_null=True)
    radius = Length()
    circle_vertices = Integer(value_range=range(6, 128))
    bevel_width = Length()
    bevel_segments = Integer(value_range=range(1, 32))

    def render(self) -> None:
        base_circle = addCircle(
            vertices=self.circle_vertices,
            radius=self.radius,
            fill_type="NGON",
        )
        with Edit(base_circle) as edit:
            # wide bottom
            edit.extrude()
            Transform.move((0, 0, self.h1))
            # indentation
            edit.extrude()
            Transform.move((0, 0, self.h2 / 3))
            edit.extrude()
            Transform.move((0, 0, self.h2 / 3))
            Transform.scale((self.scale, self.scale, 0))
            edit.extrude()
            Transform.move((0, 0, self.h2 / 3))
            inv_scale = 1 / self.scale
            Transform.scale((inv_scale, inv_scale, 0))
            # upper part
            edit.extrude()
            Transform.move((0, 0, self.h3))
            edit.smooth_faces()
        Bevel(
            Objects.active,
            width=self.bevel_width,
            segments=self.bevel_segments,
            limit_method="ANGLE",
        ).apply()

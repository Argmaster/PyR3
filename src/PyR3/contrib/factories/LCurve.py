# -*- coding: utf-8 -*-
from __future__ import annotations

import math

from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Boolean, Integer
from PyR3.factory.fields.Select import Select
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import addCircle, addPlane
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
    diameter = Length()
    cross_section = Select(
        "Square",
        "Circle",
        default=0,
    )
    material = BSDF_Material()

    def render(self) -> None:
        if self.cross_section == "Square":
            base = addPlane(
                size=self.diameter,
                rotation=(0, -math.pi, 0),
            )
        else:
            base = addCircle(
                radius=self.diameter / 2,
                rotation=(0, -math.pi, 0),
            )
        if self.bend:
            with Edit(base) as edit:
                edit.extrude()
                BASE_Z_OFFSET = (
                    self.total_heigh - self.bend_radius - self.diameter / 2
                )
                Transform.move((0, 0, BASE_Z_OFFSET))
                rotation_step = (math.pi / 2) / self.bend_segments
                RADIUS = self.bend_radius - self.diameter / 2

                def x_function(x):
                    RADIUS * math.sin(x) / 4

                def y_function(y):
                    RADIUS * math.cos(y) / 4

                for i in range(self.bend_segments):
                    rotation_angle = rotation_step * i
                    edit.extrude()
                    Transform.rotate(-rotation_step, "Y")
                    X = x_function(rotation_angle)
                    Y = y_function(rotation_angle)
                    Transform.move((X, 0, Y))
                edit.extrude()
                Transform.move((self.total_width - self.bend_radius, 0, 0))

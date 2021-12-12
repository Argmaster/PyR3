# -*- coding: utf-8 -*-
from __future__ import annotations

import math

# from PyR3.contrib.factories.SCurve import SCurve
from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Boolean, Integer
from PyR3.factory.fields.Sequence import HomotypeSequence
from PyR3.factory.fields.Struct import Struct
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.context import Objects
from PyR3.shortcut.material import apply_BSDF_material_params
from PyR3.shortcut.mesh import addCube
from PyR3.shortcut.modifiers import Array, Bevel
from PyR3.shortcut.transform import move, rotate, scale


class PinConfig(Struct):
    include = Boolean(default=False)
    pin_count = Integer(value_range=range(0, 1025), default=0)
    begin_offset = Length(default=0)
    total_width = Length(default=0)
    total_height = Length(default=0)
    total_depth = Length(default=0)
    lower_length = Length(default=0)
    upper_length = Length(default=0)
    steps = Integer(value_range=range(4, 128), default=5)
    thickness = Length(default=0)
    material = BSDF_Material(default={})


class Controller(MeshFactory):
    """Micro controller mesh factory."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "1.0.0"

    box_size = HomotypeSequence(Length(), length=3)
    box_material = BSDF_Material()
    box_offset = Length()
    bevel_count = Integer(value_range=range(0, 64))
    bevel_width = Length()

    pinsXY = PinConfig()
    pins_XY = PinConfig()
    pinsX_Y = PinConfig()
    pins_X_Y = PinConfig()

    def render(self) -> None:
        self.add_box()
        self.add_pins()

    def add_box(self):
        ob = addCube()
        scale(self.box_size).apply_scale()
        Bevel(
            ob,
            offset_type="OFFSET",
            segments=self.bevel_count,
            width=self.bevel_width,
        ).apply()
        move((0, 0, self.box_offset)).apply_transform()
        apply_BSDF_material_params(Objects.active, self.box_material)

    def add_pins(self):
        X, Y, _ = self.box_size
        if self.pinsXY.include:

            PIN_COUNT = self.pinsXY.pin_count
            BEGIN_OFFSET = self.bevel_width + self.pinsXY.begin_offset
            PIN_PADDING = (Y - 2 * BEGIN_OFFSET - self.pinsXY.total_depth) / (
                PIN_COUNT - 1
            )
            X_REPOSITION = X / 2 + self.pinsXY.total_width / 2
            Y_REPOSITION = Y / 2
            Z_REPOSITION = -self.pinsXY.total_height / 2
            PIN_PARAMS = self.pinsXY

            self.build_pin(
                PIN_COUNT,
                BEGIN_OFFSET,
                PIN_PADDING,
                X_REPOSITION,
                Y_REPOSITION,
                Z_REPOSITION,
                PIN_PARAMS,
            )

    def build_pin(
        self,
        PIN_COUNT,
        BEGIN_OFFSET,
        PIN_PADDING,
        X_REPOSITION,
        Y_REPOSITION,
        Z_REPOSITION,
        PIN_PARAMS,
    ):
        self.build_external_direct_map(
            "PyR3.contrib.factories.SCurve.SCurve", PIN_PARAMS
        )
        rotate(math.pi, "Z").apply_rotation()
        move(
            (X_REPOSITION, Y_REPOSITION - BEGIN_OFFSET, Z_REPOSITION)
        ).apply_transform()
        Array(
            Objects.selected[0],
            constant_offset_displace=(0, -PIN_PADDING, 0),
            count=PIN_COUNT,
        ).apply()

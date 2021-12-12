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

    pins_aY_posX = PinConfig()
    pins_aY_negX = PinConfig()
    pins_aX_posY = PinConfig()
    pins_aX_negY = PinConfig()

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
        # Among Y axis
        if self.pins_aY_posX.include:
            PIN_Y_PADDING = -(Y - 2 * self.pins_aY_posX.begin_offset) / (
                self.pins_aY_posX.pin_count - 1
            )
            HALF_PIN_WIDTH = self.pins_aY_posX.total_width / 2

            self.build_pin(
                self.pins_aY_posX.pin_count,
                0,
                PIN_Y_PADDING,
                X_REPOSITION=X / 2 + HALF_PIN_WIDTH,
                Y_REPOSITION=Y / 2 - self.pins_aY_posX.begin_offset,
                Z_REPOSITION=-self.pins_aY_posX.total_height / 2,
                PIN_PARAMS=self.pins_aY_posX,
                ROTATION=math.pi,
            )

        if self.pins_aY_negX.include:
            PIN_Y_PADDING = -(Y - 2 * self.pins_aY_posX.begin_offset) / (
                self.pins_aY_posX.pin_count - 1
            )
            HALF_PIN_WIDTH = self.pins_aY_posX.total_width / 2

            self.build_pin(
                self.pins_aY_negX.pin_count,
                0,
                PIN_Y_PADDING,
                X_REPOSITION=-X / 2 - HALF_PIN_WIDTH,
                Y_REPOSITION=Y / 2 - self.pins_aY_posX.begin_offset,
                Z_REPOSITION=-self.pins_aY_posX.total_height / 2,
                PIN_PARAMS=self.pins_aY_posX,
                ROTATION=0,
            )

        # Among X axis
        if self.pins_aX_posY.include:

            PIN_X_PADDING = -(X - 2 * self.pins_aX_posY.begin_offset) / (
                self.pins_aX_posY.pin_count - 1
            )
            HALF_PIN_WIDTH = self.pins_aX_posY.total_width / 2

            self.build_pin(
                self.pins_aX_posY.pin_count,
                PIN_X_PADDING,
                0,
                X_REPOSITION=X / 2 - self.pins_aX_posY.begin_offset,
                Y_REPOSITION=Y / 2 + HALF_PIN_WIDTH,
                Z_REPOSITION=-self.pins_aX_posY.total_height / 2,
                PIN_PARAMS=self.pins_aX_posY,
                ROTATION=math.pi / 2,
            )

        if self.pins_aX_negY.include:

            PIN_X_PADDING = -(X - 2 * self.pins_aX_negY.begin_offset) / (
                self.pins_aX_negY.pin_count - 1
            )
            HALF_PIN_WIDTH = self.pins_aX_negY.total_width / 2

            self.build_pin(
                self.pins_aX_negY.pin_count,
                PIN_X_PADDING,
                0,
                X_REPOSITION=X / 2 - self.pins_aX_negY.begin_offset,
                Y_REPOSITION=-Y / 2 - HALF_PIN_WIDTH,
                Z_REPOSITION=-self.pins_aX_negY.total_height / 2,
                PIN_PARAMS=self.pins_aX_negY,
                ROTATION=-math.pi / 2,
            )

    def build_pin(
        self,
        COUNT,
        PIN_X_PADDING,
        PIN_Y_PADDING,
        X_REPOSITION,
        Y_REPOSITION,
        Z_REPOSITION,
        PIN_PARAMS,
        ROTATION,
    ):
        self.build_external_direct_map(
            "PyR3.contrib.factories.SCurve.SCurve", PIN_PARAMS
        )
        rotate(ROTATION, "Z").apply_rotation()
        move(
            (
                X_REPOSITION,
                Y_REPOSITION,
                Z_REPOSITION,
            )
        ).apply_transform()
        Array(
            Objects.selected[0],
            constant_offset_displace=(PIN_X_PADDING, PIN_Y_PADDING, 0),
            count=COUNT,
        ).apply()

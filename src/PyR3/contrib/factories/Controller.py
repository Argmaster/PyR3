# -*- coding: utf-8 -*-
from __future__ import annotations

# from PyR3.contrib.factories.SCurve import SCurve
from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Boolean, Integer
from PyR3.factory.fields.Sequence import HomotypeSequence
from PyR3.factory.fields.Struct import Struct
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.mesh import addCube
from PyR3.shortcut.transform import Transform


class PinConfig(Struct):
    include = Boolean(default=False)
    pin_count = Integer(value_range=range(0, 1025), default=0)
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
    bevel_count = Integer(value_range=range(0, 64))
    bevel_depth = Length()

    pinsXY = PinConfig()
    pins_XY = PinConfig()
    pinsX_Y = PinConfig()
    pins_X_Y = PinConfig()

    def render(self) -> None:
        addCube()
        Transform.scale((1, 1, 1))
        print(self.pinsXY.material)

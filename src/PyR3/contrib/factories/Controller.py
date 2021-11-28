# -*- coding: utf-8 -*-
from __future__ import annotations

from PyR3.contrib.factories.SCurve import SCurve
from PyR3.factory.fields.BSDF_Material import BSDF_Material
from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.Sequence import HomotypeSequence
from PyR3.factory.fields.Struct import Struct
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.mesh import addCube
from PyR3.shortcut.transform import Transform


class Controller(MeshFactory):
    """Micro controller mesh factory."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "1.0.0"

    box_size = HomotypeSequence(Length(), length=3)
    box_material = BSDF_Material()
    bevel_count = Integer(value_range=range(0, 64))
    bevel_depth = Length()

    class PinConfig(Struct):
        pin_count = Integer(value_range=range(0, 1025))
        total_width = Length()
        total_height = Length()
        total_depth = Length()
        lower_length = Length()
        upper_length = Length()
        steps = Integer(value_range=range(4, 128))
        thickness = Length()
        material = BSDF_Material()

    pins_xy = PinConfig()
    pins__xy = PinConfig()
    pins_x_y = PinConfig()
    pins__x_y = PinConfig()

    def render(self) -> None:
        addCube()
        Transform.scale()
        SCurve(self.pin_cfg.dict()).render()

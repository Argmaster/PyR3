# -*- coding: utf-8 -*-
from __future__ import annotations

from PyR3.factory.fields.Number import Boolean
from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory


class LCurve(MeshFactory):
    """MF capable of generating straight or L like bend shaped (commonly used
    as pins for microchips)."""

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "1.0.0"

    total_width = Length()
    total_heigh = Length()
    bend = Boolean(default=False)

    def render(self) -> None:
        pass

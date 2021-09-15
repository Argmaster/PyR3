# -*- coding: utf-8 -*-

from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory


class CapacitorCase(MeshFactory):
    """
    Generates cylindrical meshes looking similar to electrolytic capacitor cases.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = [0, 0, 1]

    height = Length()
    radius = Length()

    def render(self) -> None:
        pass

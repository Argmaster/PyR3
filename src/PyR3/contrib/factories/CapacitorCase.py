# -*- coding: utf-8 -*-

from PyR3.factory.fields.Unit import Length
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import addCircle
from PyR3.shortcut.transform import Transform


class CapacitorCase(MeshFactory):
    """
    Generates cylindrical meshes looking similar to electrolytic capacitor cases.
    """

    __author__ = "Krzysztof Wiśniewski"
    __version__ = "0.0.0"

    height = Length()
    radius = Length()

    def render(self) -> None:
        base_circle = addCircle(
            radius=self.radius,
        )
        with Edit(base_circle) as edit:
            edit.extrude()
            Transform.move((0, 0, 1))

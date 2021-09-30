# -*- coding: utf-8 -*-
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.String import String


class MeshFactorySubclass(MeshFactory):

    a = Integer(value_range=range(1, 5))
    b = String(default="name")

    def render(self):
        return super().render()
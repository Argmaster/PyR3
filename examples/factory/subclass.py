# -*- coding: utf-8 -*-
from PyR3.bpy import bpy
from PyR3.factory.fields.Number import Integer
from PyR3.factory.fields.String import String
from PyR3.factory.MeshFactory import MeshFactory
from PyR3.shortcut.mesh import addCube


class MeshFactorySubclass(MeshFactory):

    size = Integer(value_range=range(1, 5))
    name = String(default="name")

    def render(self):
        cube: bpy.types.Object = addCube(size=self.size)
        cube.name = self.name
        # cube was just created so it's already selected

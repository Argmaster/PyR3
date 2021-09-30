# -*- coding: utf-8 -*-
from PyR3.shortcut.context import temporarily_selected, Objects

print(Objects.selected)  # Objects[bpy.data.objects['Cube']]
cube = Objects.selected[0]

with temporarily_selected(*Objects.all()):
    print(Objects.selected)
    # Objects[bpy.data.objects['Cube'], bpy.data.objects['Light'], bpy.data.objects['Camera']]

print(Objects.selected)  # Objects[bpy.data.objects['Cube']]

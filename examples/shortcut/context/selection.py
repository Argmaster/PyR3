# -*- coding: utf-8 -*-
from PyR3.shortcut.context import Objects
from PyR3.shortcut.mesh import addCube

# Deselects contents of current scene: default cube, light source and camera
Objects.deselect_all()
# Create new cube, uses shortcut from mesh module
cube = addCube()
# Select single object - our newly created cube
Objects.select(cube)
# prints Objects[bpy.data.objects['Cube.001']]
print(Objects.selected)

# selects everything in scene
Objects.select_all()
# Now Objects.selected is a longer sequence:
# Objects[bpy.data.objects['Cube'], bpy.data.objects['Light'],...]
print(Objects.selected)

# Lets now see whats currently active:
print(Objects.active)  # <bpy_struct, Object("Cube.001") at 0x4b39578>
# We can change it to light source existing in scene:
light_source = Objects.selected[1]
Objects.active = light_source
print(Objects.active)  # <bpy_struct, Object("Light") at 0x43a19b8>

# We can also use contents of Object.selected to alter selection:
selected = Objects.selected
selected.pop()
selected.pop(0)
selected.select_only_contained()
# Now it will print only Objects[bpy.data.objects['Light'], bpy.data.objects['Camera']]
print(Objects.selected)

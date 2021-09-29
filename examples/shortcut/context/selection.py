from PyR3.shortcut.context import Objects
from PyR3.shortcut.mesh import addCube

# deselects contents of current scene
# default cube, light source and camera
Objects.deselect_all()
# create new cube
cube = addCube()
# select single object
Objects.select(cube)
# now cube is selected
print(Objects.selected)
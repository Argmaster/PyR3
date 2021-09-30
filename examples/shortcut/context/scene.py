# -*- coding: utf-8 -*-
from PyR3.shortcut.context import delScene
from PyR3.shortcut.context import getScene
from PyR3.shortcut.context import listScenes
from PyR3.shortcut.context import newScene
from PyR3.shortcut.context import setScene
from PyR3.shortcut.context import wipeScenes

# First lets see our current scene:
print(getScene())  # <bpy_struct, Scene("Scene") at 0x41a0828>
# Now lets create new one:
newScene()
# And see list of all existing scenes
print(listScenes())  # [bpy.data.scenes['Scene'], bpy.data.scenes['Scene.001']]
# Then we can destroy _all_ of them and use new empty scene
wipeScenes()
print(listScenes())  # [bpy.data.scenes['Scene.001']]
# You can also manually set current scene:
old_scene = getScene()
newScene()
new_scene = getScene()
print(getScene() == new_scene) # True
setScene(old_scene)
print(getScene() == old_scene) # True
# deletes current scene
delScene()
print(getScene() == new_scene) # True




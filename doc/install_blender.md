# Installing precompiled binaries of _bpy_ (blender) provided in this repository


*Download [appropriate zip archive](https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries) for your operating system, version of python You are using must resemble one noted in zip file name. Unpack the zip archive somewhere, it should contain one folder, called `blender`.*

*You can also build blender yourself from source, see [this](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule) for windows, and [this](https://github.com/Argmaster/pyr3/blob/main/doc/linux_compilation.md) for linux, as wiki.blender.org explanation failed for me.*

### Windows installation

_Python packages are compatible within a minor release ie. 3.9.4 is compatible with 3.9.5 but not with 3.8.4 or 3.10_

1. Copy **all** the files from `blender` folder *(or bin, if you have compiled blender yourself)*, **without** the `2.93` folder into _site-packages_ folder of Your python installation.
2. Place `2.93` folder in same folder where Your python is installed _(where python.exe and it's libraries are located)_, even if You are using **venv**.
   You can now remove `blender` folder created in step 1.

### Linux installation

1. Copy **all** the files **and** `2.93` folder from **blender** *(or bin, if you have compiled blender yourself)* into _site-packages_ folder of Your python installation.

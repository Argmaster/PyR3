# Installing blender compiled as python module.

### This guide was made with blender v2.93 and CPython 3.9.5

_Python packages are compatible within a minor release ie. **3.9.4** `is` compatible with **3.9.5** but `not` with **3.8.4** or **3.10**_
### Manual compilation
_You can build blender yourself from source, see [this](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule) for windows, and [this](https://github.com/Argmaster/pyr3/blob/main/doc/linux_compilation.md) for linux, as wiki.blender.org explanation failed for me._

_After compilation you can follow one of installation guides below. `bin` folder from build directory will be used instead of one from zip/tar file._


### Using precompiled binaries

_Download [appropriate zip/tar archive](https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries) for your operating system and python. Unpack the zip archive somewhere, `bin` folder contained inside will be used in further steps._

#### Windows installation

[bpy-2.93-win10x64-py-3.9.5.zip](https://github.com/Argmaster/pyr3/releases/download/bpy-binaries/bpy-2.93-win10x64-py-3.9.5.zip)

1. Copy **all** the files from `bin`, **without** the `2.93` folder into _site-packages_ folder of Your python installation.
2. Place `2.93` folder in same folder where Your python is installed _(where python.exe and it's libraries are located)_, even if You are using **venv**.
   You can now remove unpacked folder created in pre-step.

#### Linux installation

[bpy-2.93-linux64-py-3.9.tar.gz](https://github.com/Argmaster/pyr3/releases/download/bpy-binaries/bpy-2.93-linux64-py-3.9.tar.gz)

1. Copy **all** the files **and** `2.93` folder from `bin` into _site-packages_ folder of Your python installation.

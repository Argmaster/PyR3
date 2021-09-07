# Installing precompiled binaries of _bpy_ (blender) provided in this repository

### Windows installation

0. Download [appropriate zip archive](https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries) for windows, version of python You are using must resemble one noted in zip file name.

_Python packages are compatible within a minor release ie. 3.9.4 is compatible with 3.9.5 but not with 3.8.4 or 3.10_

1. Unpack the zip archive somewhere, it should contain one folder, called `blender`. Enter this folder, it should contain few _dll_ files and `2.93` folder.
2. Copy all the files, **without** the `2.93` folder, into _site-packages_ folder of Your python installation.
3. Place `2.93` folder in same folder where Your python is installed _(where python.exe and it's libraries are located)_, even if You are using **venv**.
   You can now remove `blender` folder created in step 1.

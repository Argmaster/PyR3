# Installing precompiled binaries of *bpy* (blender) provided in this repository

0. Download [appropriate zip archive](https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries) depending on Your operating system and python version.
1. Unpack the zip archive somewhere, it should contain one folder, called `blender`. Enter this folder, it should contain few files and `3.0` folder.
2. Copy all the files, **without** the `3.0` folder, into *site-packages* folder of Your python installation.
3. Place `3.0` folder in same folder where Your python is installed *(where python.exe and it's libraries are located)*, even if You are using **venv**.
You can now remove `blender` folder created in step 1.
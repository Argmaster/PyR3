============
Installation
============
PyR3 is officially available at Python Package Index, therefore you can use PIP to install it
Type following into your command line::

    pip install PyR3

and hit enter.

Side Effects
============

This package installs Blender compiled as Python module for Python it is ran with.

Appropriate bpy binaries will be automatically downloaded from `here <https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries>`_
in form of tar.gz archive. Downloaded file will be placed in *side-packages/..* (folder containing side-packages).

However, if you provide appropriate archive (name is important) in this location manually, it will
be used instead of downloading. Therefore no internet connection will be needed
first time PyR3 gets invoked. After installation tar.gz file is deleted, regardless of its origin.

When initializer script is invoked, it unpacks files from tar.gz archive in appropriate places,
which differ depending on operating system:

* on **Windows** 2.93 folder will end up next to python executable you are using (even if you are using virtual environment, its necessary to place it there) and rest of the files will be copied to `site-packages`,

* on **Linux** tar archive will be unpacked into *site-packages* folder.

PyR3's blender installation behavior has direct impact over package removal,
simply calling pip uninstall PyR3 will leave bpy installed.
Files downloaded and unpacked by PyR3 at runtime have to be removed manually, if one wants to
remove all traces of PyR3.

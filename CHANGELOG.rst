
Changelog
=========

0.0.0 (2021-09-27)
------------------

* First release on PyPI.

0.1.0 (2021-10-01)
------------------

* Added Modifiers: Boolean, Array, Solidify and Bevel
* Added fromPyData()
* Improved documentation
* Added example files
* Added dark theme to docs

0.1.1 (2021-10-01)
------------------

* Hotfix of missing dependencies in package

0.1.2 (2021-10-01)
------------------

* Hotfix of export/import API

0.2.0 (2021-10-03)
------------------

* Added materials shortcuts
* Updated documentation
* Bpy is no longer automatically installed
* Bpy can be now installed via PyR3.install_bpy script

0.2.3 (2021-10-03)
------------------

* Updated documentation

0.3.0 (2021-10-21)
------------------

* Introduced new development pipeline
* Extendent usage documentation
* .blend1 files no longer can be imported/exported with shortcuts.io functions
* Added LibraryManager class for managing 3D component libraries
* Added LibraryObject class responsible for managing libraries
* Added LibraryInfoV1_0_0 and ModelInfoV1_0_0 classes for ``__lib__.yaml`` version 1.0.0 files validation
* Added way to extend set tags of a model from ``__lib__.yaml`` - via ``__user__.yaml``
* Added documentation for newest features
* Added MeshProject class and project configuration convention
* Added PlaceFile class which can parse place file and convert it into MeshProject file
* Added PyR3.construct CLI for operating on MeshProject files
* Added PyR3.meshlib CLI for operating on mesh libraries

0.4.0 (2021-11-08)
------------------

* Updated implementation of PyR3.contrib.factories.CapacitorCase
* Added API and CLI for rendering single models using MeshFactories
* Added Remesh modifier class
* Added SCurve MeshFactory subclass

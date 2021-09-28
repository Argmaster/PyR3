========
Overview
========

.. start-badges

|docs| |travis| |codecov| |version| |wheel| |supported-versions| |supported-implementations| |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pyr3/badge/?style=flat
    :target: https://pyr3.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/Argmaster/pyr3.svg?branch=v0.0.0
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/Argmaster/pyr3

.. |codecov| image:: https://codecov.io/gh/Argmaster/pyr3/branch/main/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/github/Argmaster/pyr3

.. |version| image:: https://img.shields.io/pypi/v/PyR3.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/PyR3

.. |wheel| image:: https://img.shields.io/pypi/wheel/PyR3.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/PyR3

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/PyR3.svg
    :alt: Supported versions
    :target: https://pypi.org/project/PyR3

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/PyR3.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/PyR3

.. |commits-since| image:: https://img.shields.io/github/commits-since/Argmaster/pyr3/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/Argmaster/pyr3/compare/v0.0.0...main

.. end-badges

The PyR3 package serves two purposes:
    - provides blender in form of python package (bpy)
    - contains useful shortcuts and abstractions over bpy API

**This software is completely free to use: is released under MIT license.**


Side Effects
============

Using this package has side effects that the user should be aware of.
Side effects will occurs after PyR3 is imported (PyR3.__init__ is run).

This package installs Blender compiled as Python module for Python it is ran with.
Appropriate bpy binaries will be automatically downloaded from `here <https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries>`_.
It also means that first time this package is imported, internet connection
have to be available, otherwise import will fail.
Binaries can be downloaded manually from `here <https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries>`_.
To make PyR3 use them instead and avoid downloading at runtime, place tar.gz
file at *side-packages/..* (folder containing side-packages) of your python/virtual environment.
Thats the same place, where PyR3 places tar archive it downloads.
After installation tar.gz file is deleted.

When initializer script is invoked, it installs files from tar.gz archive in appropriate places,
which differ depending on operating system:
- on Windows 2.93 folder will end up next to python executable you are using (even if you are using virtual environment, its necessary to place it there) and rest of the files will be copied to `site-packages`,
- on Linux tar archive will be unpacked in to *site-packages* folder.

Installation
============
PyR3 is available on Python Package Index and can be installed automatically with **pip**::

    pip install PyR3

You can also install the in-development version from github with::

    pip install https://github.com/Argmaster/pyr3/archive/main.zip


Removing PyR3
==============

When you are removing PyR3, first use pip to uninstall actual package::

    pip install PyR3

then you will have to remove the files created by PyR3 that were needed to install bpy.
See Side Effects for description where to find bpy files created by PyR3.


Documentation
=============

Documentation is available on-line at https://pyr3.readthedocs.io/


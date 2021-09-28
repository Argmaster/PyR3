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

A set of tools extending the capabilities of bpy (blender as a python module).

Blender as python module is bundled in wheel distributions of this package.
Importing PyR3 will cause initializer script install bpy in required way into
your python. It's important to be aware that in case of removal of this package,
it will be necessary to remove blender manually. Also, blender is installed differently
depending on platform - on linux all blender files end up in site-packages - when on Windows
it is necessary to place 2.93 (Resources folder) in same directory as python.exe when other binaries
ends up in site-packages.

**This software is completely free to use: is released under MIT license.**

Installation
============
PyR3 is available on Python Package Index and can be installed automatically with **pip**
::

    pip install PyR3

You can also install the in-development version from github with::

    pip install https://github.com/Argmaster/pyr3/archive/main.zip


Documentation
=============

Documentation is available on-line at https://pyr3.readthedocs.io/


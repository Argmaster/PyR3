.. image:: https://raw.githubusercontent.com/Argmaster/pyr3/main/docs/_static/logo_wide.png

========
Overview
========

.. start-badges

|docs| |travis| |codecov| |version| |wheel| |supported-versions| |supported-implementations| |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pyr3/badge/?style=flat
    :target: https://pyr3.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/Argmaster/pyr3.svg?branch=v0.1.2
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/Argmaster/pyr3/v0.1.2.svg
    :alt: Commits since latest release
    :target: https://github.com/Argmaster/pyr3/compare/v0.1.2...main

.. end-badges

The PyR3 package serves two purposes:
    - provides blender in form of python package (bpy)
    - contains useful shortcuts and abstractions over bpy API

**This software is completely free to use: is released under MIT license.**


Installation
============
PyR3 is available on Python Package Index and can be installed automatically with **pip**::

    pip install PyR3

You can also install the in-development version from github with::

    pip install https://github.com/Argmaster/pyr3/archive/main.zip


Side Effects
============

Using this package has side effects that the user should be aware of.
Side effects will occurs after PyR3 is imported (PyR3.__init__ is run).

See Side Effects on Installation page for more in-depth description.

Because we often want those side effects to be guaranteed to happen,
I encourage you to instead of simply importing bpy, use following

.. code-block:: python

    from PyR3.bpy import bpy

It will cause PyR3.__init__ to be always invoked before you request bpy.

Documentation
=============

Documentation is available on-line at https://pyr3.readthedocs.io/

You can also build documentation yourself using tox::

    git clone hhttps://github.com/Argmaster/pyr3.git
    cd PyR3
    tox -e docs


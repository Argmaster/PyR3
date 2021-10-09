.. image:: https://raw.githubusercontent.com/Argmaster/pyr3/main/docs/_static/logo_wide.png

========
Overview
========

.. start-badges

|docs| |tests| |codecov| |version| |wheel| |supported-versions| |supported-implementations| |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pyr3/badge/?style=flat
    :target: https://pyr3.readthedocs.io/
    :alt: Documentation Status

.. |tests| image:: https://github.com/Argmaster/pyr3/actions/workflows/main.yml/badge.svg
    :target: https://github.com/Argmaster/pyr3
    :alt: Workflow Status

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/Argmaster/pyr3/v0.2.2.svg
    :alt: Commits since latest release
    :target: https://github.com/Argmaster/pyr3/compare/v0.2.2...main

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


Complicated bpy requirement
===========================

Unlike previous releases, since 0.2.2 bpy is no longer automatically installed
when importing PyR3, as this solution was not what's expected by typical developer.

Now to install bpy automatically you have to invoke **PyR3.install_bpy** module
.. code-block:: bash

    python -m PyR3.install_bpy

Or you can use install_bpy_lib() function from this module.
After installing bpy it has to be manually uninstalled.
It may happen that in future releases some uninstall script
will be created, but for now manual removal is the only way.

Documentation
=============

Documentation is available on-line at https://pyr3.readthedocs.io/

You can also build documentation yourself using tox::

    git clone hhttps://github.com/Argmaster/pyr3.git
    cd PyR3
    tox -e docs


.. image:: https://raw.githubusercontent.com/Argmaster/pyr3/main/docs/_static/logo_wide.png

##########
 Overview
##########

.. image:: https://img.shields.io/github/license/Argmaster/PyR3
   :alt: Package License
   :target: https://pypi.org/project/PyR3

.. image:: https://readthedocs.org/projects/pyr3/badge/?style=flat
   :alt: Documentation Status
   :target: https://PyR3.readthedocs.io/

.. image:: https://github.com/Argmaster/PyR3/actions/workflows/draft_release.yaml/badge.svg?style=flat
   :alt: Workflow Status
   :target: https://github.com/Argmaster/PyR3

.. image:: https://github.com/Argmaster/PyR3/actions/workflows/release_pr_tests.yaml/badge.svg?style=flat
   :alt: Workflow Status
   :target: https://github.com/Argmaster/PyR3

.. image:: https://codecov.io/gh/Argmaster/PyR3/branch/main/graph/badge.svg?token=VM09IHO13U
   :alt: Code coverage stats
   :target: https://codecov.io/gh/Argmaster/PyR3

.. image:: https://img.shields.io/github/v/release/Argmaster/PyR3?style=flat
   :alt: GitHub release (latest by date)
   :target: https://github.com/Argmaster/PyR3/releases/tag/v0.4.3

.. image:: https://img.shields.io/github/commit-activity/m/Argmaster/PyR3
   :alt: GitHub commit activity
   :target: https://github.com/Argmaster/PyR3/commits/main

.. image:: https://img.shields.io/github/issues-pr/Argmaster/PyR3?style=flat
   :alt: GitHub pull requests
   :target: https://github.com/Argmaster/PyR3/pulls

.. image:: https://img.shields.io/github/issues-pr-closed-raw/Argmaster/PyR3?style=flat
   :alt: GitHub closed pull requests
   :target: https://github.com/Argmaster/PyR3/pulls

.. image:: https://img.shields.io/github/issues-raw/Argmaster/PyR3?style=flat
   :alt: GitHub issues
   :target: https://github.com/Argmaster/PyR3/issues

.. image:: https://img.shields.io/github/languages/code-size/Argmaster/PyR3
   :alt: GitHub code size in bytes
   :target: https://github.com/Argmaster/PyR3

.. image:: https://img.shields.io/pypi/v/PyR3?style=flat
   :alt: PyPI Package latest release
   :target: https://pypi.org/project/PyR3

.. image:: https://img.shields.io/pypi/wheel/PyR3?style=flat
   :alt: PyPI Wheel
   :target: https://pypi.org/project/PyR3

.. image:: https://img.shields.io/pypi/pyversions/PyR3?style=flat
   :alt: Supported versions
   :target: https://pypi.org/project/PyR3

.. image:: https://img.shields.io/pypi/implementation/PyR3?style=flat
   :alt: Supported implementations
   :target: https://pypi.org/project/PyR3

The PyR3 package serves two purposes:
   -  provides blender in form of python package (bpy)
   -  contains useful shortcuts and abstractions over bpy API

**This package is released under MIT license**. Be aware that
dependencies might be using different licenses.

**************
 Installation
**************

PyR3 is available on Python Package Index and can be installed
automatically with **pip**:

.. code::

   pip install PyR3

You can also install the in-development version from github with:

.. code::

   pip install https://github.com/Argmaster/pyr3/archive/main.zip

*****************************
 Complicated bpy requirement
*****************************

Unlike previous releases, since 0.2.2 bpy is no longer automatically
installed when importing PyR3, as this solution was not what's expected
by typical developer.

Now to install bpy automatically you have to invoke **PyR3.install_bpy**
module::

   python -m PyR3.install_bpy

Or you can use install_bpy_lib() function from this module. After
installing bpy it has to be manually uninstalled. It may happen that in
future releases some uninstall script will be created, but for now
manual removal is the only way.

***************
 Documentation
***************

Documentation is available on-line at https://pyr3.readthedocs.io/

You can also build documentation yourself using tox:

.. code::

   git clone hhttps://github.com/Argmaster/pyr3.git
   cd PyR3
   tox -e docs

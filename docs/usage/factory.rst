
PyR3.factory
============

This package provides MeshFactory class which should
be subclassed to create specialized mesh factories
and fields sub-package containing predefined field
types that can be used in MeshFactory subclass.

Creating MeshFactory subclasses
-------------------------------

Example below presents mesh factory which creates cube with size depending on
integer field value, with custom name.

.. literalinclude:: ../../examples/factory/subclass.py
   :language: python
   :caption: examples/factory/subclass.py


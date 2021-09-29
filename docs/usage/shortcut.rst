
PyR3.shortcut
=============

This subpackage contains useful abstractions and shortcuts over blender API,
which are used multiple times in other parts of PyR3, but it is mend also
for public access and use.


Managing selected and active objects with PyR3.shortcut.context.Objects
-----------------------------------------------------------------------

Deselecting all object in current scene.

.. code-block:: python

    from PyR3.shortcut.context import Objects

    Objects.deselect_all()


Seecting 
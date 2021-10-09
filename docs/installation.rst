##############
 Installation
##############

PyR3 is officially available at Python Package Index, therefore you can
use PIP to install it Type following into your command line:

.. code::

   pip install PyR3

and hit enter. PyR3 requires bpy (blender as python module) to run, but
has no automatic way to install it on users PC. You can either install
it manually or use PyR3.install_bpy to download and install it
automatically. For later, see next section.

****************
 Installing bpy
****************

PyR3.install_bpy script contained in this package can be used to install
bpy for currently used python.

Appropriate bpy binaries will be automatically downloaded from `here
<https://github.com/Argmaster/pyr3/releases/tag/bpy-binaries>`_ in form
of tar.gz archive. Downloaded file will be placed in *side-packages/..*
(folder containing side-packages).

However, if you provide appropriate archive (name is important) in this
location manually, it will be used instead of downloading. Therefore no
internet connection will be needed first time PyR3 gets invoked. After
installation tar.gz file is deleted, regardless of its origin.

When initializer script is invoked, it unpacks files from tar.gz archive
in appropriate places, which differ depending on operating system:

-  on **Windows** 2.93 folder will end up next to python executable you
   are using (even if you are using virtual environment, its necessary
   to place it there) and rest of the files will be copied to
   `site-packages`,

-  on **Linux** tar archive will be unpacked into *site-packages*
   folder.

*****************
 Package Removal
*****************

To remove PyR3 from your python use:

.. code::

   pip uninstall PyR3

However if you have installed bpy with PyR3 (or any other way) above
command wont remove it. Files which belong to bpy have to be deleted
manually, and can be found in places described in Installing bpy
section.

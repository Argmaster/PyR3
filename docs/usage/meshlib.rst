##############
 PyR3.meshlib
##############

`All files used as examples are contained in this repository, under
corresponding relative paths.`

LibraryManager class contained in this sub-package is designed to work
as high-level tool to retrieving static models from specially prepared
libraries.

*************************
 How to create libraries
*************************

The core of every library is a ``__lib__.yaml`` file, containing all
library metadata, including list of models within library. Library
assets can be structured however you want them to, as long as you are
able to provide paths to them, relative to ``__lib__.yaml`` file
directory.

********************************
 ``__lib__.yaml`` file contents
********************************

``__lib__.yaml`` file is a static configuration file written in YAML.
This file have to contain following keys in top-level dictionary:

-  ``version`` currently only version 1.0.0 is a valid value
-  ``name`` library name, It is highly recommended to make it as unique
   as possible
-  ``author`` author's name / nick
-  ``description`` library description
-  ``lib_version`` library version, a semantic versioning compatible
   version string
-  ``model_list`` list of dictionaries containing model metadata,
   explained below.

Model information
=================

To define a model, you have to use dictionary, containing following set
of keys:

-  ``hash`` model SHA1 hash encoded as base64, if not of a valid length,
   will be recalculated and replaced
-  ``version`` model version, a semantic versioning compatible version
   string
-  ``author`` model author's name / nick
-  ``description`` model description
-  ``file`` file path, relative to folder containing ``__lib__.yaml``
   file
-  ``tags`` model tag list, later they can be used to find all models
   with matching tag, tags don't have to be unique
-  ``scale`` indicates how the model is scaled in comparison to real
   size.
-  ``icon`` path to an icon file for this model, relative to folder containing ``__lib__.yaml``
      file

Example ``__lib__.yaml`` file:

.. literalinclude:: ../../tests/test_meshlib/test_lib/__lib__.yaml
   :language: yaml
   :caption: tests/test_meshlib/test_lib/__lib__.yaml

****************************************
 Extending list of model tags as a user
****************************************

It is possible to extend set of tags assigned to model described in
``__lib__.yaml`` file without modifying this file. You can achieve it by
adding ``__user__.yaml`` file in the same directory as ``__lib__.yaml``.
``__user__.yaml`` file contains YAML code, with top-level dictionary
containing only ``tags`` key. This key maps to a nested dictionary with
keys being hashes of models (as a base64 encoded strings). The values
are also dictionaries with following keys:

-  ``tags`` a list of string tags extending base tag set of a model
-  ``comment`` a human readable comment

Example ``__user__.yaml`` file:

.. literalinclude:: ../../tests/test_meshlib/test_lib/__user__.yaml
   :language: yaml
   :caption: tests/test_meshlib/test_lib/__user__.yaml

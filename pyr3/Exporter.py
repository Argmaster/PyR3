# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy


class Exporter:

    """This class is a container for set of scene exporting functions.
    They operate on global scene, therefore they are all static.
    Constants userfull for calling of those functions are also available here.
    All of those functions are based on coresponding functions from bpy
    module, and accept same set of kwargs as those from bpy.
    See https://docs.blender.org/api/current/bpy.ops.export_scene.html for lists
    of accepted keyword arguments for each function.
    """

    GLB = "GLB"
    GLTF_EMBEDDED = "GLTF_EMBEDDED"
    GLTF_SEPARATE = "GLTF_SEPARATE"

    @staticmethod
    def glTF(filepath: str, export_format: str = GLB, **kwargs):
        """Export scene as glTF 2.0 file.

        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: str
        :param export_format: Format, Output format and embedding options. Binary is most efficient, but JSON (embedded or separate) may be easier to edit later, defaults to GLB
        :type export_format: str, optional
        :param `**kwargs`: Additional arguments for exporting.
        """
        bpy.ops.export_scene.gltf(filepath, export_format=export_format, **kwargs)

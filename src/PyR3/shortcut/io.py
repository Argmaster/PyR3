"""IO module provides import/export functions with ability to recognize
file format from filename. It's limited but handy solution, hence available here.
Recognized formats are:

- **GLB** : glTF Binary (.glb), Exports a single file, with all data packed in binary form.

- **GLTF** : glTF Embedded (.gltf), Exports a single file, with all data packed in JSON.

- **FBX** : Autodesk Filmbox (.fbx)

- **X3D** : Extensible 3D Graphics (.x3d)

- **OBJ** : Wavefront OBJ (.obj)

- **PLY** : Polygon File Format / Polygon File Format (.ply)

- **STL** : STL triangle mesh data (.stl)

- **BLEND** / **BLEND1** : Blender file format (.blend/.blend1) be aware that it causes to overwrite current scene on import.
"""
# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path as _Path

from bpy.ops import export_mesh as _export_mesh
from bpy.ops import export_scene as _export_scene
from bpy.ops import import_mesh as _import_mesh
from bpy.ops import import_scene as _import_scene
from bpy.ops import wm as _wm


__export = {
    "GLB": lambda filepath, **kwargs: _export_scene.gltf(
        filepath=filepath, export_format="GLB", **kwargs
    ),
    "GLTF": lambda filepath, **kwargs: _export_scene.gltf(
        filepath=filepath, export_format="GLTF_EMBEDDED", **kwargs
    ),
    "FBX": _export_scene.fbx,
    "X3D": _export_scene.x3d,
    "OBJ": _export_scene.obj,
    "PLY": _export_mesh.ply,
    "STL": _export_mesh.stl,
    "BLEND": _wm.save_as_mainfile,
    "BLEND1": _wm.save_as_mainfile,
}


def export_to(filepath: str, **kwargs):
    """Export all objects into file. Format is determined from file extension.
    kwargs will be forwarded to bpy method call coresponding to selected format.

    :param filepath: _Path to the file to export to.
    :type filepath: str
    :raises KeyError: if format is not recognized.
    """
    format = _Path(filepath).suffix[1:].upper()
    try:
        __export.get(format)(filepath=str(filepath), **kwargs)
    except KeyError:
        raise KeyError(f"Format {format} is not supported.") from None


__import = {
    "GLB": lambda filepath, **kwargs: _import_scene.gltf(
        filepath=filepath, import_format="GLB", **kwargs
    ),
    "GLTF": lambda filepath, **kwargs: _import_scene.gltf(
        filepath=filepath, import_format="GLTF_EMBEDDED", **kwargs
    ),
    "FBX": _import_scene.fbx,
    "X3D": _import_scene.x3d,
    "OBJ": _import_scene.obj,
    "PLY": _import_mesh.ply,
    "STL": _import_mesh.stl,
    "BLEND": _wm.open_mainfile,
    "BLEND1": _wm.open_mainfile,
}


def import_from(filepath: str, **kwargs):
    """Import data from file. Format is determined from file extension.
    kwargs will be forwarded to bpy method call coresponding to selected format.

    :param filepath: _Path to file to import.
    :type filepath: str
    :raises KeyError: if format is not recognized.
    """
    format = _Path(filepath).suffix[1:].upper()
    try:
        __import.get(format)(filepath=str(filepath), **kwargs)
    except KeyError:
        raise KeyError(f"Format {format} is not supported.") from None

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

from pathlib import Path

from bpy.ops import export_mesh
from bpy.ops import export_scene
from bpy.ops import import_mesh
from bpy.ops import import_scene
from bpy.ops import wm

export_gltf = export_scene.gltf
export_fbx = export_scene.fbx
export_obj = export_scene.obj
export_x3d = export_scene.x3d
export_ply = export_mesh.ply
export_stl = export_mesh.stl
export_blend = wm.save_as_mainfile


__export = {
    "GLB": lambda filepath, **kwargs: export_scene.gltf(
        filepath, export_format="GLB", **kwargs
    ),
    "GLTF": lambda filepath, **kwargs: export_scene.gltf(
        filepath, export_format="GLTF_EMBEDDED", **kwargs
    ),
    "FBX": export_scene.fbx,
    "X3D": export_scene.x3d,
    "OBJ": export_scene.obj,
    "PLY": export_mesh.ply,
    "STL": export_mesh.stl,
    "BLEND": wm.save_as_mainfile,
    "BLEND1": wm.save_as_mainfile,
}


def ExportGlobal(filepath: str, **kwargs):
    """Export all objects as format recognized from filename.

    :param filepath: Path to the file to export to.
    :type filepath: str
    :raises KeyError: if format is not recognized.
    """
    _export(filepath, use_selection=True, **kwargs)


def ExportSelected(filepath: str, **kwargs):
    """Export currently selected objects as format recognized from filename.

    :param filepath: Path to the file to export to.
    :type filepath: str
    :raises KeyError: if format is not recognized.
    """
    _export(filepath, use_selection=True, **kwargs)


def _export(filepath, use_selection, **kwargs):
    format = Path(filepath).suffix[1:].upper()
    try:
        __export.get(format)(filepath, use_selection=use_selection, **kwargs)
    except KeyError:
        raise KeyError(f"Format {format} is not supported.") from None


import_gltf = import_scene.gltf
import_fbx = import_scene.fbx
import_obj = import_scene.obj
import_x3d = import_scene.x3d
import_ply = import_mesh.ply
import_stl = import_mesh.stl
import_blend = wm.save_as_mainfile


__import = {
    "GLB": lambda filepath, **kwargs: import_scene.gltf(
        filepath, import_format="GLB", **kwargs
    ),
    "GLTF": lambda filepath, **kwargs: import_scene.gltf(
        filepath, import_format="GLTF_EMBEDDED", **kwargs
    ),
    "FBX": import_scene.fbx,
    "X3D": import_scene.x3d,
    "OBJ": import_scene.obj,
    "PLY": import_mesh.ply,
    "STL": import_mesh.stl,
    "BLEND": wm.open_mainfile,
    "BLEND1": wm.open_mainfile,
}


def Import(filepath: str, **kwargs):
    """Import 3D mesh or scene, depending on file extension.

    :param filepath: Path to file to import.
    :type filepath: str
    :raises KeyError: if format is not recognized.
    """
    format = Path(filepath).suffix[1:].upper()
    try:
        __import.get(format)(filepath, **kwargs)
    except KeyError:
        raise KeyError(f"Format {format} is not supported.") from None

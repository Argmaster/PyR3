# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import yaml

from PyR3.factory.MeshFactory import MeshFactory, import_factory
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to


def build_from_file(src_file: Path, save_path: Path):
    """Build mesh using configuration from file. Later mesh is saved to
    save_path.

    :param src_file: source configuration file.
    :type src_file: Path
    :param save_path: destination save path.
    :type save_path: Path
    """
    with src_file.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    build_and_save(
        data.get("type", "python").lower(),
        data["class"],
        data["params"],
        save_path,
    )


def build_and_save(
    generator_type: str,
    class_: str | MeshFactory,
    params: dict,
    save_path: Path,
):
    if generator_type == "python":
        build_python(class_, params)
    else:
        raise RuntimeError(
            f"Unknown generator type '{generator_type}' selected."
        )
    export_to(filepath=save_path)


def build_python(class_: str | MeshFactory, params: dict):
    wipeScenes()
    if isinstance(class_, str):
        class_ = import_factory(class_)
    class_(**params).render()

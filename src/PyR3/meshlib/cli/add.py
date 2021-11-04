# -*- coding: utf-8 -*-
import shutil
from getpass import getuser
from glob import glob
from pathlib import Path
from typing import Dict, List, Tuple

import click
from rich.console import Console

from PyR3.meshlib.lib_obj import LibraryObject, load
from PyR3.meshlib.lib_obj.model_info import (
    DEFAULT_ICON_SYMBOL,
    ModelInfoV1_0_0,
)

CONSOLE = Console()


@click.argument(
    "lib_file_path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "--mesh-ver",
    default="1.0.0",
    help="Mesh version to be used in models metadata.",
)
@click.option(
    "--author",
    default=getuser(),
    help="Mesh version to be used in models metadata.",
)
@click.option(
    "--glob",
    is_flag=True,
    help="Interpret model paths as glob patterns.",
)
@click.argument("model_paths", nargs=-1)
def add(
    lib_file_path: Path, glob: bool, model_paths: Tuple[str], **model_info_pref
):
    models_path_triples = _resolve_model_paths(
        lib_file_path, glob, model_paths
    )
    library_object = load(lib_file_path)
    _copy_and_append_models(
        lib_file_path,
        models_path_triples,
        model_info_pref,
        library_object,
    )
    library_object.save_in_place()
    CONSOLE.print(
        "Library file saved.",
        style="green",
    )


def _resolve_model_paths(
    lib_file_path: Path, glob: bool, model_paths: Tuple[str]
) -> List[Tuple[Path, Path, str]]:
    models_dir = lib_file_path.parent / "models"
    if glob:
        paths = _resolve_paths_as_glob(models_dir, model_paths)
    else:
        paths = _resolve_paths_as_paths(models_dir, model_paths)
    if len(paths) > 0:
        models_dir.mkdir(0o777, False, True)
    return paths


def _resolve_paths_as_glob(
    models_dir: Path, model_glob_patterns: Tuple[str]
) -> List[Tuple[Path, Path, str]]:
    paths = []
    for glob_pattern in model_glob_patterns:
        for path in glob(glob_pattern):
            path = Path(path)
            paths.append(
                (
                    path.resolve(),
                    (models_dir / path.name).resolve(),
                    f"models/{path.name}",
                )
            )
    return paths


def _resolve_paths_as_paths(
    models_dir: Path, model_paths: Tuple[str]
) -> List[Tuple[Path, Path, str]]:
    paths = []
    for path in model_paths:
        path = Path(path)
        paths.append(
            (
                path.resolve(),
                (models_dir / path.name).resolve(),
                f"models/{path.name}",
            )
        )
    return paths


def _copy_and_append_models(
    lib_file_path: Path,
    models_path_triples: List[Tuple[Path, Path, str]],
    model_info_pref: Dict[str, str],
    library_object: LibraryObject,
):
    for index, (source, destination, relative_path) in enumerate(
        models_path_triples
    ):
        CONSOLE.print(
            f"\n > Processing model object no {index}.", style="blue"
        )
        if not destination.exists():
            try:
                CONSOLE.print(
                    f"Copying model file from '{source}' to '{destination}'",
                )
                shutil.copy2(source, destination)
            except FileNotFoundError as e:
                CONSOLE.print(
                    f"Failed to copy file: {e}.",
                    style="red",
                )
                continue
            model_info = ModelInfoV1_0_0(
                directory=lib_file_path.parent,
                hash="",
                version=model_info_pref.get("mesh_ver"),
                author=model_info_pref.get("author"),
                description="",
                tags=[source.name.split(".")[0]],
                scale=1.0,
                file=relative_path,
                icon=DEFAULT_ICON_SYMBOL,
            )
            library_object.info.model_list.append(model_info)
            CONSOLE.print(
                "Successfully appended new model to library!", style="green"
            )
            _pretty_print_mi(model_info)
        else:
            CONSOLE.print(
                f"    Model '{source}' already contained in library {library_object.info.name}.",
                style="yellow",
            )


def _pretty_print_mi(model_info):
    CONSOLE.print(
        f"    Hash:    [yellow]{model_info.hash}[/yellow]",
        highlight=False,
    )
    CONSOLE.print(
        f"    Tags:    [yellow]{model_info.tags}[/yellow]",
        highlight=False,
    )
    CONSOLE.print(
        f"    Relpath: [yellow]{model_info.file}[/yellow]",
        highlight=False,
    )

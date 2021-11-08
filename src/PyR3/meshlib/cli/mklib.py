# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

import click
from rich.console import Console

from PyR3.meshlib.cli.const import EXIT_CODE
from PyR3.meshlib.lib_obj import LibraryObject

CONSOLE = Console()


@click.argument(
    "lib_file_path",
    type=Path,
)
@click.option(
    "--name",
    prompt="Library name",
    help="Name for the library.",
)
@click.option(
    "--author",
    prompt="Author's name",
    help="Name of the library author.",
)
@click.option(
    "--description",
    default="",
    help="Library description.",
)
@click.option(
    "--lib-version",
    prompt="Library version",
    help="Library version string.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force overwrite of destination folder.",
)
def mklib(lib_file_path: Path, force: bool, **kwargs):
    lib_file_path = _clean_lib_file_path(lib_file_path, force)
    LibraryObject(
        lib_file_path=lib_file_path,
        version="1.0.0",
        **kwargs,
        model_list=[],
    ).save_in_place()


def _clean_lib_file_path(lib_file_path: Path, force: bool):
    if lib_file_path.name != "__lib__.yaml":
        library_dir = lib_file_path
        lib_file_path = lib_file_path / "__lib__.yaml"
    else:
        library_dir = lib_file_path.parent
    if force:
        shutil.rmtree(library_dir, True)
    if library_dir.exists():
        if len(os.listdir(library_dir)) != 0:
            CONSOLE.print(
                f"Folder {library_dir} already exits, remove it or change destination folder and retry.",
                style="red",
            )
            exit(EXIT_CODE.MKLIB_FOLDER_EXISTS)
    else:
        library_dir.mkdir(0o777, True, False)
    return lib_file_path

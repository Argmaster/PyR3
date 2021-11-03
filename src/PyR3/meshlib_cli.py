# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import sys
from getpass import getuser
from glob import glob
from pathlib import Path
from typing import Any, Dict, List

import yaml
from rich.console import Console

from PyR3.meshlib.lib_obj.lib_info import LibraryInfoV1_0_0
from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0

CONSOLE = Console()


def main(args: List[str]):
    args = parse_args(args)
    if args.no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
    if args.command == "mklib":
        run_make_library(args)
    elif args.command == "extend":
        run_extend_library(args)


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser("meshlib_cli")
    parser.add_argument(
        "--no-rich",
        "-r",
        dest="no_rich",
        action="store_true",
        default=False,
        help="Output only raw text without highlighting.",
    )
    subparsers = parser.add_subparsers(dest="command")
    # from_dir_parser
    from_dir_parser = subparsers.add_parser("mklib")
    from_dir_parser.add_argument(
        "library_name",
        help="Name of output library (can be modified manually later).",
    )
    from_dir_parser.add_argument(
        "--author",
        default=getuser(),
        help="Library author.",
    )
    from_dir_parser.add_argument(
        "models_globs",
        nargs="+",
        help="Glob patterns for model matching.",
    )
    from_dir_parser.add_argument(
        "--force",
        "-f",
        dest="force",
        action="store_true",
        default=False,
        help="Force operation to complete despite errors (can cause silent overwrites of directories and files.).",
    )
    # lib_validator
    validate_parser = subparsers.add_parser("extend")
    validate_parser.add_argument(
        "library_path",
        help="Path to __lib__.yaml file to which you want to append.",
    )
    return parser.parse_args(args)


def run_make_library(args):
    library_dir_path = get_library_dir(args.library_name, args.force)
    library_file_path = library_dir_path / "__lib__.yaml"
    li = LibraryInfoV1_0_0(
        lib_file_path=library_file_path,
        name=args.library_name,
        author=args.author,
        description="",
        lib_version="1.0.0",
        model_list=get_and_copy_models(args, library_dir_path),
    )
    with library_file_path.open("w", encoding="utf-8") as file:
        yaml.dump(li.dict(), file, sort_keys=False)


def get_list_of_model_paths(models_globs: List[str]):
    full_path_list = []
    for glob_pattern in models_globs:
        full_path_list.extend(glob(glob_pattern))
    return [Path(path) for path in full_path_list]


def get_library_dir(library_name: str, force: bool = False):
    library_dir_path = Path(library_name).resolve()
    if library_dir_path.exists() and len(os.listdir(library_dir_path)) != 0:
        if force:
            CONSOLE.print(
                f"Folder {library_dir_path} have been permanently removed.",
                style="red",
            )
            shutil.rmtree(library_dir_path)
        else:
            CONSOLE.print(
                f"Folder {library_dir_path} already exits, remove it or change package name and retry.",
                style="red",
            )
            exit(1)
    CONSOLE.print(
        f"Created '{library_dir_path}'.",
        style="blue",
    )
    library_dir_path.mkdir(0o777, True, True)
    return library_dir_path


def get_and_copy_models(
    args: argparse.Namespace, lib_dir: Path
) -> List[Dict[str, Any]]:
    output_model_data_list = []
    model_paths = get_list_of_model_paths(args.models_globs)
    for model_path in model_paths:
        destination = lib_dir / model_path.name
        CONSOLE.print(
            f"> Copying [green]'{model_path}'[/green] to [blue]'{destination}'[/blue].",
            highlight=False,
        )
        shutil.copy(model_path, destination)
        model_data = ModelInfoV1_0_0(
            directory=lib_dir,
            hash="",
            version="1.0.0",
            author=args.author,
            description="",
            tags=[model_path.name.split(".")[0]],
            scale=1.0,
            file=model_path.name,
            icon="__default_icon__",
        ).dict()
        CONSOLE.print(
            f"    Hash:    [yellow]{model_data['hash']}[/yellow]",
            highlight=False,
        )
        CONSOLE.print(
            f"    Tags:    [yellow]{model_data['tags']}[/yellow]",
            highlight=False,
        )
        CONSOLE.print(
            f"    Relpath: [yellow]{model_data['file']}[/yellow]",
            highlight=False,
        )
        output_model_data_list.append(model_data)
    return output_model_data_list


def run_extend_library(args: argparse.Namespace):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])

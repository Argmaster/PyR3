# -*- coding: utf-8 -*-
import argparse
import shutil
import sys
from getpass import getuser
from glob import glob
from pathlib import Path
from typing import List

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
    full_path_list = _join_glob_results(args.models_globs)
    if args.command == "from-dir":
        _construct_library_from_dir(args, full_path_list)


def _construct_library_from_dir(args, full_path_list):
    LIBRARY_DIR = Path(args.library_name).resolve()
    _create_library_dir(LIBRARY_DIR)
    LIB_FILE_PATH = LIBRARY_DIR / "__lib__.yaml"
    MODEL_LIST = _create_model_list(full_path_list, LIBRARY_DIR)
    li = LibraryInfoV1_0_0(
        lib_file_path=LIB_FILE_PATH,
        name=args.library_name,
        author=getuser(),
        description="",
        lib_version="1.0.0",
        model_list=[m.dict() for m in MODEL_LIST],
    )
    with LIB_FILE_PATH.open("w", encoding="utf-8") as file:
        yaml.dump(li.dict(), file)


def _create_library_dir(LIBRARY_DIR):
    if LIBRARY_DIR.exists():
        CONSOLE.print(
            f"Folder {LIBRARY_DIR} already exits, remove it or change package name and retry.",
            style="red",
        )
        exit(1)
    else:
        LIBRARY_DIR.mkdir(0o777, True, True)


def _join_glob_results(models_globs: List[str]):
    full_path_list = []
    for glob_pattern in models_globs:
        full_path_list.extend(glob(glob_pattern))
    return full_path_list


def _create_model_list(
    model_paths: List[str], lib_dir: Path
) -> List[ModelInfoV1_0_0]:
    mi_list = []
    for model_path in model_paths:
        model_path = Path(model_path)
        shutil.copy(model_path, lib_dir / model_path.name)
        mi = ModelInfoV1_0_0(
            directory=lib_dir,
            hash="",
            version="1.0.0",
            author=getuser(),
            description="",
            tags=[model_path.name.split(".")[0]],
            scale=1.0,
            file=model_path.name,
            icon="__default_icon__",
        )
        mi_list.append(mi)
    return mi_list


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
    from_dir_parser = subparsers.add_parser("from-dir")
    from_dir_parser.add_argument(
        "library_name",
        help="Name of output library (can be modified manually later).",
    )
    from_dir_parser.add_argument(
        "models_globs",
        nargs="+",
        help="Glob patterns for model matching.",
    )
    # lib_validator
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("-x")
    return parser.parse_args(args)


if __name__ == "__main__":
    main(sys.argv[1:])

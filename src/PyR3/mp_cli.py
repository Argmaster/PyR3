# -*- coding: utf-8 -*-
import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import List, Optional

import pydantic
import yaml
from rich.console import Console

from PyR3.construct.mp import MeshProject
from PyR3.meshlib import (
    LibraryManager,
    get_paths_from_env,
    get_paths_from_file,
)

CONSOLE = Console()


class RUN_MODE(Enum):
    CHECK = 1
    RESOLVE = 2
    CONSTRUCT = 3


def main(args: List[str]):
    args = parse_args(args)
    if args.no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
    if args.mode == RUN_MODE.CHECK:
        run_check_cli(args)
    elif args.mode == RUN_MODE.RESOLVE:
        run_resolve_cli(args)
    elif args.mode == RUN_MODE.CONSTRUCT:
        run_construct_cli(args)


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser("PyR3.mp_cli")
    parser.add_argument(
        "project_file",
        type=Path,
        help="Path to Mesh Project (.mp.yaml) file.",
    )
    mutually_exclusive = parser.add_mutually_exclusive_group(
        required=True,
    )
    mutually_exclusive.add_argument(
        "--check",
        action="store_const",
        dest="mode",
        const=RUN_MODE.CHECK,
        help="Run only in check (validation) mode.",
    )
    mutually_exclusive.add_argument(
        "--resolve",
        action="store_const",
        dest="mode",
        const=RUN_MODE.RESOLVE,
        help="Run only to resolve tags into hashes wherever possible.",
    )
    mutually_exclusive.add_argument(
        "--construct",
        action="store_const",
        dest="mode",
        const=RUN_MODE.CONSTRUCT,
        help="Run in construction mode.",
    )
    parser.add_argument(
        "--no-rich",
        "-r",
        dest="no_rich",
        action="store_true",
        default=False,
        help="Output only raw text without highlighting.",
    )
    parser.add_argument(
        "--ml-paths",
        nargs="+",
        dest="ml_paths",
        default=None,
        help="List of meshlib paths to include in library searching.",
    )
    parser.add_argument(
        "--ml-path-file",
        dest="ml_path_file",
        default=None,
        help="List of meshlib paths to include in library searching.",
    )
    parser.add_argument(
        "--ignore-env",
        "-i",
        dest="ignore_env",
        action="store_true",
        default=False,
        help="Ignore environmental constant MESHLIBPATH while looking for mesh libraries.",
    )
    parser.add_argument("--extend-m")
    return parser.parse_args(args)


def run_check_cli(args: argparse.Namespace):
    if (mp := load_mesh_project(args.project_file)) is None:
        exit(1)
    CONSOLE.print("Running in check mode.", style="#407cff")
    print_mp_metadata(mp)
    library_manager = load_libraries(args)
    _check_mp_components_availability(library_manager, mp)


def load_mesh_project(mp_path: str) -> Optional[MeshProject]:
    try:
        mp = MeshProject.load(mp_path)
    except yaml.scanner.ScannerError as e:
        CONSOLE.print(
            "Mesh project file found, but contains invalid YAML source code.",
            style="red",
        )
        CONSOLE.print(e)
        return None
    except FileNotFoundError:
        CONSOLE.print(
            "Mesh project file not found.",
            style="#eb4d26",
        )
        return None
    except pydantic.ValidationError as e:
        CONSOLE.print(
            "Mesh project file found, and contains valid YAML but fields provided are not fully valid.",
            style="yellow",
        )
        CONSOLE.print(e)
        return None
    else:
        CONSOLE.print(
            "Mesh project file found and contains valid YAML.", style="green"
        )
        return mp


def print_mp_metadata(mp: MeshProject):
    SEP = "[#56606e]" + "-" * CONSOLE.width + "[/#56606e]"
    CONSOLE.print(SEP)
    CONSOLE.print(f"Format version: {mp.format_version}")
    CONSOLE.print("Project:", style="blue")
    CONSOLE.print(f"    Name: [blue]{mp.project_name}[/blue]")
    CONSOLE.print(f"    Version: {mp.project_version}")
    LF = "\n      "
    PADDED_DESC = mp.description.replace("\n", "\n       ")
    CONSOLE.print(
        f"    Description:{LF if mp.description else ''} [#4abd5f]{PADDED_DESC}[/#4abd5f]"
    )
    CONSOLE.print(f"    Scale: {mp.scale}")
    CONSOLE.print(f"    Components: {len(mp.component_list)} total.")
    CONSOLE.print(SEP)


def load_libraries(args: List[str]):
    CONSOLE.print("Loading mesh libraries...", style="green")
    FULL_PATH = _get_full_meshlib_path_list(args)
    LIBRARY = LibraryManager(FULL_PATH)
    if len(LIBRARY.LIBS) == 0:
        CONSOLE.print(
            "No meshlib libraries found.",
            style="#e0de12",
        )
    else:
        CONSOLE.print(
            f"Successfully loaded total of {len(LIBRARY.LIBS)} libraries.",
            style="green",
        )
    return LIBRARY


def _get_full_meshlib_path_list(args):
    ML_PATHS = _clean_ml_paths(args)
    ML_PATH_FILE = _get_ml_path_file_paths(args)
    ENV_PATHS = get_paths_from_env()
    CONSOLE.print(
        f"Including total of {len(ENV_PATHS)} paths listed in environmental variable MESHLIBPATH.",
        style="#469de0",
    )
    FULL_PATH = ML_PATHS + ML_PATH_FILE + ENV_PATHS
    return FULL_PATH


def _clean_ml_paths(args):
    if args.ml_paths is None:
        ML_PATHS = []
    else:
        ML_PATHS = [str(Path(path).resolve()) for path in args.ml_paths]
        CONSOLE.print(
            f"Including total of {len(ML_PATHS)} paths listed for --ml-paths:",
            style="#469de0",
        )
    for path in ML_PATHS:
        CONSOLE.print(" -", path, style="#95b5f5 italic")
    return ML_PATHS


def _get_ml_path_file_paths(args):
    if args.ml_path_file is None:
        ml_path_file = Path("meshlib.path")
        if not ml_path_file.exists():
            CONSOLE.print(
                "No meshlib.path file found.",
                style="#469de0",
            )
            return []
    else:
        ml_path_file = Path(args.ml_path_file).resolve()
        if not ml_path_file.exists():
            if ml_path_file.is_file():
                CONSOLE.print(
                    f"File '{ml_path_file}' doesn't exist, paths from it wont be included.",
                    style="red",
                )
            else:
                CONSOLE.print(
                    f"Path '{ml_path_file}' doesn't point to a file, paths from it wont be included.",
                    style="red",
                )
            return []
    ML_PATH_FILE_PATHS = get_paths_from_file(ml_path_file)

    CONSOLE.print(
        f"Including total of {len(ML_PATH_FILE_PATHS)} paths from '{ml_path_file}' file:",
        style="#469de0",
    )
    for path in ML_PATH_FILE_PATHS:
        CONSOLE.print(" -", path, style="#95b5f5 italic")
    return ML_PATH_FILE_PATHS


def _check_mp_components_availability(
    library_manager: LibraryManager, mp: MeshProject
):

    SEP = "[#56606e]" + "-" * CONSOLE.width + "[/#56606e]"
    CONSOLE.print(SEP)
    CONSOLE.print(
        "Performing mesh project component validation:", style="#FFFFFF"
    )
    for index, component in enumerate(mp.component_list):
        model_list = library_manager.get_for_project_component(component)
        CONSOLE.print(f"Component [blue]{component.symbol}[/blue] ({index}):")
        CONSOLE.print(
            f"  Hash: {component.hash if component.hash else '[red]no hash provided[/red]'}"
        )
        CONSOLE.print(
            f"  Tags: {component.tags if component.tags else '[red]no tags provided[/red]'}"
        )

        if len(model_list) > 1:
            CONSOLE.print(
                (
                    "    Model tags specified for component are ambiguous, "
                    f"found total of {len(model_list)} matching models."
                ),
                style="yellow",
            )
        elif len(model_list) == 0:
            CONSOLE.print(
                "    No matching models have been found.",
                style="red",
            )
        else:
            CONSOLE.print(
                f"    No models for component {component.symbol} ({index}) have been found.",
                style="#1ad64c",
            )


def run_resolve_cli(args: argparse.Namespace):
    pass


def run_construct_cli(args: argparse.Namespace):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])

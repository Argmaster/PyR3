# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Tuple

import click
import pydantic
import yaml
from rich.console import Console

from PyR3.construct.cli.const import EXIT_CODE
from PyR3.construct.mp import MeshProject
from PyR3.meshlib import (
    LibraryManager,
    get_meshlib_path_from_env,
    get_meshlib_path_from_file,
)

CONSOLE = Console()


@click.argument(
    "project_path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
@click.argument(
    "meshlib_paths",
    default=(),
)
@click.option(
    "--ml-path-file",
    help="Path leading to a meshlib.path file containing list of paths to search for libraries.",
)
@click.option(
    "--ignore-env",
    "-i",
    is_flag=True,
    help="Ignore environmental constant MESHLIBPATH while looking for mesh libraries.",
)
def check(
    project_path: Path,
    meshlib_paths: Tuple[str],
    ml_path_file: str,
    ignore_env: bool,
):
    CONSOLE.print("Running in check mode.", style="#407cff")
    mp = load_mesh_project(project_path)
    print_mp_metadata(mp)
    library_manager = load_libraries(meshlib_paths, ml_path_file, ignore_env)
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
        exit(EXIT_CODE.MESHPROJECT_FILE_INVALID_YAML_SYNTAX)
    except FileNotFoundError:
        CONSOLE.print(
            "Mesh project file not found.",
            style="#eb4d26",
        )
        exit(EXIT_CODE.MESHPROJECT_FILE_NOT_FOUND)
    except pydantic.ValidationError as e:
        CONSOLE.print(
            "Mesh project file found, and contains valid YAML but fields provided are not fully valid.",
            style="yellow",
        )
        CONSOLE.print(e)
        exit(EXIT_CODE.MESHPROJECT_INVALID_FIELD_VALUE)
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


def load_libraries(ml_paths: Tuple[str], ml_path_file: str, ignore_env: bool):
    CONSOLE.print("Loading mesh libraries...", style="green")
    FULL_PATH = _get_full_meshlib_path_list(ml_paths, ml_path_file, ignore_env)
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


def _get_full_meshlib_path_list(
    ml_paths: Tuple[str], ml_path_file: str, ignore_env: bool
):
    ML_PATHS = _clean_ml_paths(ml_paths)
    ML_PATH_FILE = _get_ml_path_file_paths(ml_path_file)
    if not ignore_env:
        ENV_PATHS = get_meshlib_path_from_env()
    CONSOLE.print(
        f"Including total of {len(ENV_PATHS)} paths listed in environmental variable MESHLIBPATH.",
        style="#469de0",
    )
    FULL_PATH = ML_PATHS + ML_PATH_FILE + ENV_PATHS
    return FULL_PATH


def _clean_ml_paths(ml_paths: Tuple[str]):
    if ml_paths is None:
        ML_PATHS = []
    else:
        ML_PATHS = [str(Path(path).resolve()) for path in ml_paths]
        CONSOLE.print(
            f"Including total of {len(ML_PATHS)} paths listed for --ml-paths:",
            style="#469de0",
        )
    for path in ML_PATHS:
        CONSOLE.print(" -", path, style="#95b5f5 italic")
    return ML_PATHS


def _get_ml_path_file_paths(ml_path_file: str):
    if ml_path_file is None:
        ml_path_file = Path("meshlib.path")
        if not ml_path_file.exists():
            CONSOLE.print(
                "No meshlib.path file found.",
                style="#469de0",
            )
            return []
    else:
        ml_path_file = Path(ml_path_file).resolve()
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
    ML_PATH_FILE_PATHS = get_meshlib_path_from_file(ml_path_file)
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

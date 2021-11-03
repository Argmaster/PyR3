# -*- coding: utf-8 -*-
import argparse
import sys
from glob import glob
from typing import List

from rich.console import Console

CONSOLE = Console()


def main(args: List[str]):
    args = parse_args(args)
    if args.no_rich:
        CONSOLE.no_color = True
        CONSOLE.highlighter = None
    CONSOLE.print(args.library_name)
    CONSOLE.print(args.library_version)
    CONSOLE.print(list(glob(args.models_glob)))


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
    subparsers = parser.add_subparsers()
    # from_dir_parser
    from_dir_parser = subparsers.add_parser("from-dir")
    from_dir_parser.add_argument(
        "library_name",
        help="Name of output library (can be modified manually later).",
    )
    from_dir_parser.add_argument(
        "library_version",
        help="Description of output library (can be modified manually later).",
    )
    from_dir_parser.add_argument(
        "models_glob",
        help="Glob pattern for model matching.",
    )
    from_dir_parser.add_argument(
        "glob_interpretation",
        help="How to interpret path patterns.",
    )
    # lib_validator
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("-x")
    return parser.parse_args(args)


if __name__ == "__main__":
    main(sys.argv[1:])

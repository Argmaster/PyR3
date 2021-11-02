# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path
from typing import List

from PyR3.construct.parse_place import PlaceFile


def main(args: List[str]):
    args = parse_args(args)
    with args.place.open("r", encoding="utf-8") as file:
        place_src = file.read()
    pf = PlaceFile(args.place, place_src)
    mp = pf.to_MeshProject()
    mp.dump(args.mp)


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser("place_to_mp")
    parser.add_argument(
        "--place",
        type=Path,
        help="Path to input place file.",
    )
    parser.add_argument(
        "--mp",
        type=Path,
        help="Path to output mesh project (.mp.yaml) file.",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main(sys.argv[1:])

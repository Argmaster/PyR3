# -*- coding: utf-8 -*-
import argparse
import subprocess
import sys
from typing import List

from .fork_release import fork_branch
from .version_tag import fetch_version


def main():
    args = parse_args(sys.argv[1:])
    subprocess.run(
        ["git", "checkout", args.from_branch],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    version_tag = fetch_version("src/PyR3/__init__.py")
    fork_branch("patch", "hotfix", args.from_branch, version_tag)


def parse_args(argv: List[str]):
    parser = argparse.ArgumentParser("fork_release")
    parser.add_argument(
        "from_branch",
        help="Branch to fork hotfix from.",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    exit(main())

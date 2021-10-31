# -*- coding: utf-8 -*-
import subprocess
import sys
from glob import glob


def main():
    subprocess.run([sys.executable, "-m", "isort", "."])
    subprocess.run([sys.executable, "-m", "flake8", "."])
    subprocess.run([sys.executable, "-m", "rstfmt", "docs"])
    subprocess.run([sys.executable, "-m", "rstfmt", "README.rst"])
    for folder in ("src", "tests", "examples", "scripts"):
        subprocess.run([sys.executable, "-m", "black", folder])
    for file in glob("src/**/*.py", recursive=True):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "docformatter",
                "--in-place",
                file,
                "--docstring-length",
                "75",
                "75",
            ]
        )


if __name__ == "__main__":
    main()

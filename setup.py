#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
import sys
import platform

from setuptools import setup, Distribution


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


HAS_PLATNAME = any(["--plat-name" in string for string in sys.argv])
if HAS_PLATNAME:
    IS_LINUX = any(["manylinux1" in string for string in sys.argv])
    IS_WINDOWS = any(["win_amd64" in string for string in sys.argv])
else:
    IS_LINUX = platform.system() == "Linux"
    IS_WINDOWS = platform.system() == "Windows"


AUTHOR = "Krzysztof Wiśniewski"
EMAIL = "argmaster.world@gmail.com"
HOME_URL = "https://github.com/Argmaster/pyr3"

DESCRIPTION = (
    "A set of tools extending the capabilities of bpy (blender as a python module)."
)
LONG_DESCRIPTION = "%s\n%s" % (
    re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
        "", read("README.rst")
    ),
    re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
)

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Utilities",
]

PROJECT_URLS = {
    "Documentation": "https://pyr3.readthedocs.io/",
    "Changelog": "https://pyr3.readthedocs.io/en/latest/changelog.html",
    "Issue Tracker": "https://github.com/Argmaster/pyr3/issues",
}


if __name__ == "__main__":
    with open("src/requirements.txt") as file:
        requirements = [r.strip() for r in file.readlines()]
    setup(
        name="PyR3",
        version="0.1.2",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/x-rst",
        author=AUTHOR,
        author_email=EMAIL,
        url=HOME_URL,
        packages=["PyR3"],
        package_dir={"": "src"},
        py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        project_urls=PROJECT_URLS,
        keywords=[],
        python_requires=">=3.8",
        install_requires=requirements,
        extras_require={
            # eg:
            #   'rst': ['docutils>=0.11'],
            #   ':python_version=="2.6"': ['argparse'],
        }
    )

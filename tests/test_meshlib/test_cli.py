# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
from pathlib import Path
from unittest import TestCase

from PyR3.meshlib.cli import mklib
from PyR3.meshlib.cli.const import EXIT_CODE

DIR = Path(__file__).parent.resolve()

TEMP = DIR / ".temp"
TEMP.mkdir(0o777, True, True)


class TestMeshlibCLI(TestCase):
    def make_library(self, force: bool = False):
        LIB_PATH = TEMP / "_test_lib"
        args = [
            str(LIB_PATH / "__lib__.yaml"),
            "--name",
            "libname",
            "--author",
            "libauthor",
            "--lib-version",
            "3.3.3",
        ]
        if force:
            args.append("-f")
        mklib(args)

    def test_mklib(self):
        LIB_PATH = TEMP / "_test_lib"
        shutil.rmtree(LIB_PATH, True)
        try:
            self.make_library()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            raise RuntimeError

    def test_mklib_empty_folder_exists(self):
        LIB_PATH = TEMP / "_test_lib"
        shutil.rmtree(LIB_PATH, True)
        LIB_PATH.mkdir(0o777, True, True)
        try:
            self.make_library()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            raise RuntimeError

    def test_mklib_fail_for_existing(self):
        LIB_PATH = TEMP / "_test_lib"
        shutil.rmtree(LIB_PATH, True)
        try:
            self.make_library()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            raise RuntimeError

        try:
            self.make_library()
        except SystemExit as e:
            self.assertEqual(e.code, EXIT_CODE.MKLIB_FOLDER_EXISTS)
        else:
            raise RuntimeError

    def test_mklib_force_overwrite(self):
        LIB_PATH = TEMP / "_test_lib"
        shutil.rmtree(LIB_PATH, True)
        try:
            self.make_library()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            raise RuntimeError

        try:
            self.make_library(force=True)
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            raise RuntimeError

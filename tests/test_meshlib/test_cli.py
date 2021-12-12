# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.meshlib.cli import add, mklib
from PyR3.meshlib.cli.const import EXIT_CODE
from tests.temp_dir import TEMP_DIR

DIR = Path(__file__).parent.resolve()

TEMP = DIR / ".temp"
TEMP.mkdir(0o777, True, True)


class TestMeshlibCLI(TestCase):
    def make_library(self, dest_path: Path, force: bool = False):
        args = [
            str(dest_path),
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

    def make_temp_lib(self, LIB_PATH):
        with self.assertRaisesRegex(SystemExit, "0"):
            self.make_library(LIB_PATH)

    def test_mklib(self):
        with TEMP_DIR(DIR) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            self.make_temp_lib(LIB_PATH)

    def test_mklib_empty_folder_exists(self):
        with TEMP_DIR(DIR) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            LIB_PATH.mkdir(0o777, True, True)
            self.make_temp_lib(LIB_PATH)

    def test_mklib_fail_for_existing(self):
        with TEMP_DIR(DIR) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            LIB_PATH.mkdir(0o777, True, True)
            self.make_temp_lib(LIB_PATH)
            with self.assertRaisesRegex(
                SystemExit, str(EXIT_CODE.MKLIB_FOLDER_EXISTS)
            ):
                self.make_library(LIB_PATH)

    def test_mklib_force_overwrite(self):
        with TEMP_DIR(DIR) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            self.make_temp_lib(LIB_PATH)
            with self.assertRaisesRegex(SystemExit, "0"):
                self.make_library(LIB_PATH, force=True)

    def test_add_model_to_mesh_lib(self):
        with TEMP_DIR(DIR, delete=False) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            self.make_temp_lib(LIB_PATH)
            with self.assertRaisesRegex(SystemExit, "0"):
                add(
                    [
                        str(LIB_PATH / "__lib__.yaml"),
                        str(DIR.parent / "models" / "1N4148.glb"),
                        str(DIR.parent / "models" / "C0805.glb"),
                    ]
                )

    def test_add_model_to_mesh_lib_overides(self):
        with TEMP_DIR(DIR, delete=False) as temp_dir:
            LIB_PATH = temp_dir / "_test_lib"
            self.make_temp_lib(LIB_PATH)
            with self.assertRaisesRegex(SystemExit, "0"):
                add(
                    [
                        str(LIB_PATH / "__lib__.yaml"),
                        str(DIR.parent / "models" / "*.glb"),
                        "--glob",
                        "--author",
                        "Argmaster",
                        "--mesh-ver",
                        "4.2.3",
                    ]
                )

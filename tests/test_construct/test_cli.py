# -*- coding: utf-8 -*-
from __future__ import annotations

import subprocess
import sys
from os import chdir
from pathlib import Path
from unittest import TestCase

import yaml

from PyR3.const import CONSOLE
from PyR3.construct.cli import add, check, common_main, new
from PyR3.construct.cli.check import get_pathlist_from_file, load_libraries
from PyR3.construct.cli.const import EXIT_CODE
from PyR3.construct.mp import MeshProject
from tests.temp_dir import TEMP_DIR

CONSOLE.disable_rich()


DIR = Path(__file__).parent


class TestConstructCLI(TestCase):
    def make_test_project(
        self,
        temp_dir: Path,
        exit_code: int = 0,
        malform: bool = False,
        invalid_value: bool = False,
    ):
        lib_file_path = temp_dir / "Test_Project.mp.yaml"
        try:
            new(["Test_Project", str(lib_file_path)])
        except SystemExit as e:
            self.assertEqual(e.code, exit_code)
        if malform:
            with lib_file_path.open("r", encoding="utf-8") as file:
                content = file.read()
            with lib_file_path.open("w", encoding="utf-8") as file:
                file.write(content[len(content) // 2 :])
        elif invalid_value:
            with lib_file_path.open("r", encoding="utf-8") as file:
                content = yaml.safe_load(file)
            content["scale"] = None
            with lib_file_path.open("w", encoding="utf-8") as file:
                yaml.dump(content, file)

    def test_main_new_no_rich(self):
        with TEMP_DIR() as temp_dir:
            lib_file_path = temp_dir / "Test_Project.mp.yaml"
            self.assertRaises(
                SystemExit,
                common_main,
                ["--no-rich", "new", "Test_Project", str(lib_file_path)],
            )

    def test_main_new_with_rich(self):
        with TEMP_DIR() as temp_dir:
            lib_file_path = temp_dir / "Test_Project.mp.yaml"
            self.assertRaises(
                SystemExit,
                common_main,
                ["new", "Test_Project", str(lib_file_path)],
            )
            self.make_test_project(temp_dir, EXIT_CODE.FILE_EXISTS)

    def test_new_force_overwrite(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir)
            try:
                new(
                    [
                        "Test_Project",
                        str(temp_dir / "Test_Project.mp.yaml"),
                        "-f",
                    ]
                )
            except SystemExit as e:
                self.assertEqual(e.code, 0)

    def test_add_successful(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir)
            try:
                add(
                    [
                        str(temp_dir / "Test_Project.mp.yaml"),
                        "A1",
                        "0",
                        "0",
                        "TEST0",
                    ]
                )
            except SystemExit as e:
                self.assertEqual(e.code, 0)

    def test_add_fail_repeated_symbol(self):
        with TEMP_DIR(delete=False) as temp_dir:
            proj_path = str(temp_dir / "Test_Project.mp.yaml")
            self.make_test_project(temp_dir)
            try:
                add([proj_path, "A1", "0", "0", "TEST0"])
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            else:
                raise RuntimeError
            try:
                add([proj_path, "A1", "0", "0", "TEST1"])
            except SystemExit as e:
                self.assertEqual(
                    e.code, EXIT_CODE.COMPONENT_WITH_SYMBOL_EXISTS
                )
            else:
                raise RuntimeError
            mp = MeshProject.load(proj_path)
            self.assertTrue(len(mp.component_list) == 1)

    def test_check(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir)
            try:
                check([str(temp_dir / "Test_Project.mp.yaml")])
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            else:
                raise RuntimeError

    def test_add_and_check(self):
        with TEMP_DIR() as temp_dir:
            MP_PATH = str(temp_dir / "Test_Project.mp.yaml")
            self.make_test_project(temp_dir)
            try:
                add([MP_PATH, "A1", "0", "0", "TEST0"])
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            else:
                raise RuntimeError
            try:
                check([MP_PATH])
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            else:
                raise RuntimeError

    def test_check_malformed_yaml(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir, malform=True)
            try:
                check([str(temp_dir / "Test_Project.mp.yaml")])
            except SystemExit as e:
                self.assertEqual(
                    e.code, EXIT_CODE.MESHPROJECT_FILE_INVALID_YAML_SYNTAX
                )
            else:
                raise RuntimeError

    def test_check_invalid_value(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir, invalid_value=True)
            try:
                check([str(temp_dir / "Test_Project.mp.yaml")])
            except SystemExit as e:
                self.assertEqual(
                    e.code, EXIT_CODE.MESHPROJECT_INVALID_FIELD_VALUE
                )
            else:
                raise RuntimeError

    def test_check_file_not_found(self):
        with TEMP_DIR() as temp_dir:
            try:
                check([str(temp_dir / "Test_Project.mp.yaml")])
            except SystemExit as e:
                self.assertEqual(e.code, EXIT_CODE.MESHPROJECT_FILE_NOT_FOUND)
            else:
                raise RuntimeError

    def test_check_load_libraries(self):
        chdir(DIR / ".." / "..")
        lib_mng = load_libraries((), Path("tests/meshlib.path"), True)
        self.assertTrue(len(lib_mng.PATH) > 0)
        self.assertTrue(len(lib_mng.LIBS) > 0)

    def test__get_ml_path_file_paths(self):
        paths = get_pathlist_from_file()
        self.assertTrue(len(paths) == 0)

    def test__main__cli(self):
        with TEMP_DIR() as temp_dir:
            lib_file_path = temp_dir / "Test_Project.mp.yaml"
            cp = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "PyR3.construct",
                    "check",
                    lib_file_path,
                ]
            )
            cp.wait()
            print(cp.stdout)
            print(cp.stderr)
            self.assertEqual(cp.returncode, 2)

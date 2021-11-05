# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from PyR3.construct.cli import new
from PyR3.construct.cli.const import EXIT_CODE
from tests.temp_dir import TEMP_DIR

DIR = Path(__file__).parent


class TestConstructCLI(TestCase):
    def make_test_project(self, temp_dir: Path, exit_code: int = 0):
        try:
            new(["Test_Project", str(temp_dir / "Test_Project.mp.yaml")])
        except SystemExit as e:
            self.assertEqual(e.code, exit_code)

    def test_new_successful(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir)

    def test_new_fail_on_existing(self):
        with TEMP_DIR() as temp_dir:
            self.make_test_project(temp_dir)
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


if __name__ == "__main__":
    main()

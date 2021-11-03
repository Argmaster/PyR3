# -*- coding: utf-8 -*-
from __future__ import annotations

import os

# import shutil
from pathlib import Path
from unittest import TestCase

# from PyR3.meshlib.cli import main

DIR = Path(__file__).parent.resolve()
CWD = os.getcwd()
LIBNAME = "TO_transistor_models"


class TestMeshlibCLI(TestCase):
    def setUp(self) -> None:
        os.chdir(DIR)

    def test_mklib_():
        pass

    # def test_forcefull_creation(self):
    #     main(["mklib", LIBNAME, "models/TO*.glb", "-f"])
    #     self.assertTrue(os.path.exists(LIBNAME + "/__lib__.yaml"))
    #     shutil.rmtree(LIBNAME)

    # def test_no_force_creation_empty_folder(self):
    #     os.mkdir(LIBNAME)
    #     main(["mklib", LIBNAME, "models/TO*.glb"])
    #     self.assertTrue(os.path.exists(LIBNAME + "/__lib__.yaml"))
    #     shutil.rmtree(LIBNAME)

    # def test_no_force_creation_filled_folder(self):
    #     os.mkdir(LIBNAME)
    #     with open(LIBNAME + "/trash.txt", "w"):
    #         pass
    #     self.assertRaises(
    #         SystemExit, lambda: main(["mklib", LIBNAME, "models/TO*.glb"])
    #     )
    #     self.assertFalse(os.path.exists(LIBNAME + "/__lib__.yaml"))
    #     shutil.rmtree(LIBNAME)

    def tearDown(self) -> None:
        os.chdir(CWD)

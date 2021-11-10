# -*- coding: utf-8 -*-
import shutil

for path in (
    ".temp",
    "__pycache__",
    "htmlcov",
    "dist",
):
    shutil.rmtree(path)

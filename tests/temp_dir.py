# -*- coding: utf-8 -*-
import shutil
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def TEMP_DIR(
    root: Path = Path("."), delete: bool = True, pre_delete: bool = True
):
    temp_dir = root / ".temp"
    if pre_delete:
        shutil.rmtree(temp_dir, True)
    temp_dir.mkdir(0o777, True, True)
    yield temp_dir
    if delete:
        shutil.rmtree(temp_dir, True)

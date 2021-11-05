# -*- coding: utf-8 -*-
import shutil
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def TEMP_DIR(root: Path = Path(".")):
    temp_dir = root / ".temp"
    shutil.rmtree(temp_dir, True)
    temp_dir.mkdir(0o777, True, True)
    yield temp_dir
    shutil.rmtree(temp_dir, True)

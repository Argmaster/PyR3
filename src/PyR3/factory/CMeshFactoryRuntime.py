# -*- coding: utf-8 -*-


import subprocess
from pathlib import Path
from typing import Dict


class CMeshFactoryRuntime:

    c_mf_path: Path
    params: Dict

    def __init__(self, c_mf_path: Path, params: Dict) -> None:
        self.c_mf_path = c_mf_path
        self.params = params

    def run(self) -> None:
        process = subprocess.Popen([self.c_mf_path])
        process.stdin.write()

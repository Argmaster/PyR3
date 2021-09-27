# -*- coding: utf-8 -*-
import os
import platform
import shutil
import sys
import tarfile
from pathlib import Path

import requests

IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"


def unpack_lib():
    if check_unpack_required():
        if IS_WINDOWS:
            unpack_windows()
        elif IS_LINUX:
            unpack_linux()
        else:
            raise RuntimeError(
                "This operating system is not supported. We support only Windows and Linux."
            )


def check_unpack_required():
    try:
        import bpy
    except ImportError:
        return True
    return False


def is_installed():
    end_path = os.path.join("src", "PyR3", "unpack.py")
    if Path(__file__).__str__().endswith(end_path):
        return False
    return True


def get_python_executable_dir() -> Path:
    return Path(os.__file__).parent.parent


def get_site_packages_dir() -> Path:
    return Path(sys.prefix) / "lib" / "site-packages"


if is_installed():

    def bpy_tar_gz_path() -> Path:
        lib_dir = Path(__file__).parent.parent.parent
        if IS_WINDOWS:
            return lib_dir / "bpy_2_93-win_amd64-cp39.tar.gz"
        elif IS_LINUX:
            return lib_dir / "bpy_2_93-linux_64-cp39.tar.gz"


else:

    def bpy_tar_gz_path() -> Path:
        if IS_WINDOWS:
            path = (
                Path(__file__).parent.parent.parent
                / "lib"
                / "win"
                / "bpy_2_93-win_amd64-cp39.tar.gz"
            )
            if not os.path.exists(path):
                download_file(
                    "https://github.com/Argmaster/pyr3/releases/download/bpy-binaries/bpy_2_93-win_amd64-cp39.tar.gz",
                    path,
                )
        elif IS_LINUX:
            path = (
                Path(__file__).parent.parent.parent
                / "lib"
                / "linux"
                / "bpy_2_93-linux_64-cp39.tar.gz"
            )
            if not os.path.exists(path):
                download_file(
                    "https://github.com/Argmaster/pyr3/releases/download/bpy-binaries/bpy_2_93-linux_64-cp39.tar.gz",
                    path,
                )
        return path


def download_file(url: str, local_path: Path):
    with requests.get(url, stream=True) as r:
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def get_path_members(archive: tarfile.TarFile, path: str):
    return [member for member in archive.getmembers() if member.path.startswith(path)]


def unpack_linux():
    with tarfile.open(bpy_tar_gz_path()) as archive:
        archive.extractall(get_site_packages_dir(), members=archive.getmembers())


def unpack_windows():
    with tarfile.open(bpy_tar_gz_path()) as archive:
        folder_2_93_members = [
            member
            for member in archive.getmembers()
            if member.path.startswith("./2.93/")
        ]
        archive.extractall(get_python_executable_dir(), members=folder_2_93_members)
        other_members = [
            member
            for member in archive.getmembers()
            if not member.path.startswith("./2.93/")
        ]
        archive.extractall(get_site_packages_dir(), members=other_members)


if __name__ == "__main__":
    unpack_lib()

# -*- coding: utf-8 -*-
import base64
import hashlib
from pathlib import Path
from typing import List, Set

from packaging.version import Version

from PyR3.shortcut.io import import_from


class ModelInfoBase:
    pass


class ModelInfoV1_0_0(ModelInfoBase):

    DEFAULT_HASH_LENGTH = 128

    hash: str
    directory: Path
    version: Version
    author: str
    description: str
    tags: Set[str]
    file: str

    def __init__(
        self,
        directory: str,
        hash: str,
        version: str,
        author: str,
        description: str,
        tags: List[str],
        file: str,
    ):
        self.directory = Path(directory).resolve()
        self.hash = hash
        self.version = Version(version)
        self.author = author
        self.description = description
        self.tags = set(tags)
        self.file = Path(file)
        self._validate_import_path()
        self._calculate_hash_if_none()

    def _validate_import_path(self):
        import_path = self.import_path
        if not import_path.exists() or not import_path.is_file():
            raise RuntimeError(f"File '{import_path}' doesn't exist or is not a file.")
        if self.import_path.suffix == ".blend":
            raise RuntimeError(
                f"Loading failure: blend files ('{import_path}') can't be used as library model."
            )

    def _calculate_hash_if_none(self):
        if len(self.hash) != self.DEFAULT_HASH_LENGTH:
            with self.import_path.open("rb") as file:
                fed_algorithm = hashlib.sha1(file.read())
            hash = fed_algorithm.digest()
            self.hash = base64.b64encode(hash)

    @property
    def import_path(self) -> Path:
        return self.directory / self.file

    def load(self):
        import_from(self.import_path)

    def match_hash(self, hash: str):
        return self.hash == hash

    def match_tag(self, tag: str):
        return tag in self.tags

    def dict(self):
        return {
            "hash": self.hash,
            "version": str(self.version.public),
            "author": self.author,
            "description": self.description,
            "tags": list(self.tags),
            "file": str(self.file),
        }

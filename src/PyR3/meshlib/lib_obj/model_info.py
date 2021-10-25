# -*- coding: utf-8 -*-
import base64
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Set

from packaging.version import Version

from PyR3.shortcut.io import import_from


class ModelInfoBase:
    pass


@dataclass
class ModelInfoV1_0_0(ModelInfoBase):

    DEFAULT_HASH_LENGTH: ClassVar[int] = 28

    directory: Path = field(compare=False, repr=False)
    hash: str
    version: Version
    author: str
    description: str = field(compare=False, repr=False)
    tags: Set[str] = field(compare=False)
    file: str = field(compare=False)

    def __post_init__(self):
        self.version = Version(self.version)
        self.tags = set(self.tags)
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
            self.hash = base64.b64encode(hash).decode("utf-8")

    @property
    def import_path(self) -> Path:
        return (self.directory / self.file).resolve()

    def load(self):
        import_from(self.import_path)

    def match_hash(self, hash: str):
        return self.hash == hash

    def match_tag(self, tag: str):
        return tag in self.tags

    def dict(self):
        return {
            "hash": self.hash,
            "version": self.version.public,
            "author": self.author,
            "description": self.description,
            "tags": list(self.tags),
            "file": str(self.file),
        }

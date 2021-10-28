# -*- coding: utf-8 -*-
import base64
import hashlib
from pathlib import Path
from typing import Any, ClassVar, List, Set

from packaging.version import Version
from pydantic import BaseModel, validator

from PyR3.shortcut.io import import_from


class ModelInfoBase(BaseModel):
    pass


class ModelInfoV1_0_0(ModelInfoBase):

    DEFAULT_HASH_LENGTH: ClassVar[int] = 28

    directory: Path
    hash: str
    version: Version
    author: str
    description: str
    tags: Set[str]
    file: str

    class Config:
        arbitrary_types_allowed = True

    @validator("version", pre=True)
    def _version_as_Version_class(cls, version: str):
        return Version(version)

    @validator("tags", pre=True)
    def _tags_as_Set(cls, tags: List[str]):
        return set(tags)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
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
            self.hash = self.get_recalculated_hash()

    def get_recalculated_hash(self):
        with self.import_path.open("rb") as file:
            fed_algorithm = hashlib.sha1(file.read())
        hash = fed_algorithm.digest()
        return base64.b64encode(hash).decode("utf-8")

    @property
    def import_path(self) -> Path:
        return (self.directory / self.file).resolve()

    def load(self):
        import_from(self.import_path)

    def match_hash(self, hash: str):
        return self.hash == hash

    def match_tag(self, tag: str):
        return tag in self.tags

    def dict(self, *_, **__):
        return {
            "hash": self.hash,
            "version": self.version.public,
            "author": self.author,
            "description": self.description,
            "tags": sorted(list(self.tags)),
            "file": str(self.file),
        }

    def __hash__(self) -> int:
        return hash(self.hash)

    def __str__(self) -> str:
        return f"ModelInfoV1_0_0[{self.hash} {self.version} {self.author}]"

    __repr__ = __str__

# -*- coding: utf-8 -*-
import base64
import hashlib
from pathlib import Path
from typing import Any, ClassVar, List, Set, Union

from packaging.version import Version
from pydantic import BaseModel, validator

from PyR3.shortcut.io import import_from

DEFAULT_ICON_SYMBOL = "__default_icon__"


class ModelInfoV1_0_0(BaseModel):

    DEFAULT_HASH_LENGTH: ClassVar[int] = 28

    directory: Path
    hash: str
    version: Version
    author: str
    description: str
    tags: Set[str]
    scale: Union[float, int]
    file: str
    icon: Path

    class Config:
        arbitrary_types_allowed = True

    @validator("version", pre=True)
    def _version_as_Version_class(cls, version: str):
        return Version(version)

    @validator("tags", pre=True)
    def _tags_to_Set_type(cls, tags: List[str]):
        return set(tags)

    @validator("icon", pre=True)
    def _icon_str_path_to_Path_type(cls, icon: str):
        if icon and icon != DEFAULT_ICON_SYMBOL:
            icon_path = Path(icon)
            if not icon_path.exists():
                raise FileNotFoundError(f"File '{icon_path}' doesn't exist.")
            if not icon_path.is_file():
                raise FileNotFoundError(
                    f"Path '{icon_path}' doesn't point to file."
                )
            return icon_path
        else:
            return Path(DEFAULT_ICON_SYMBOL)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._validate_import_path()
        self._calculate_hash_if_none()

    def _validate_import_path(self):
        import_path = self.import_path
        if not import_path.exists() or not import_path.is_file():
            raise RuntimeError(
                f"File '{import_path}' doesn't exist or is not a file."
            )
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
            "icon": str(self.icon),
            "file": str(self.file),
            "scale": self.scale,
        }

    def __hash__(self) -> int:
        return hash(self.hash)

    def __str__(self) -> str:
        return f"ModelInfoV1_0_0[{self.hash} {self.version} {self.author}]"

    __repr__ = __str__

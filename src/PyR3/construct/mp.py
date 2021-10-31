# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import List

import yaml
from packaging.version import Version
from pydantic import BaseModel, validator


class ProjectComponent(BaseModel):
    symbol: str
    hash: str
    tags: List[str]
    version: str = "*"
    x: float
    y: float
    rotation: float
    is_top: bool


class MeshProject(BaseModel):

    project_file_path: Path
    format_version: Version
    project_version: Version
    project_name: str
    description: str
    scale: float
    component_list: List[ProjectComponent]

    class Config:
        extra = "ignore"
        arbitrary_types_allowed = True

    @validator("format_version", "project_version", pre=True)
    def _version_to_Version(value: str):
        return Version(value)

    @staticmethod
    def load(path: str) -> MeshProject:
        path = Path(path)
        with path.open("r", encoding="utf-8") as file:
            ob = yaml.safe_load(file)
        return MeshProject(project_file_path=path, **ob)

    def dump(self, path: str = None) -> None:
        """Serialize MeshProject as YAML project file.
        If path is none, project_file_path is going to be used.

        :param path: Path to save MeshProject file, defaults to None
        :type path: str, optional
        """
        if path is not None:
            path = Path(path)
        else:
            path = self.project_file_path
        with path.open("w", encoding="utf-8") as file:
            yaml.dump(self.dict(), file, sort_keys=False)

    def dict(self) -> dict:
        return {
            "format_version": self.format_version.public,
            "project_version": self.project_version.public,
            "project_name": self.project_name,
            "description": self.description,
            "scale": self.scale,
            "component_list": [c.dict() for c in self.component_list],
        }

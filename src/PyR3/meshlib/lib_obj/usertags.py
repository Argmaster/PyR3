# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml


def load(path: Path) -> UserTags:
    if path.exists():
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    else:
        data = {}
    return UserTags(path, data)


def dump(o: UserTags, path: Path):
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(o.dict(), file)


class UserTags:
    file_path: Path
    user_tags: Dict[str, Dict[str, str]]

    def __init__(self, file_path: str, data: Dict[str, Any]) -> None:
        self.file_path = file_path
        self.user_tags = data.get("tags", {})
        if not isinstance(self.user_tags, dict):
            raise SyntaxError(f"Invalid format of {file_path} file.")

    def get_extra_tags(self, hash_: str) -> List[str]:
        model_tags = self.user_tags.get(hash_, {})
        return model_tags.get("tags", [])

    def get_hash_with_tag(self, tag: str) -> str:
        hashes_found = []
        for hash_, extra_data in self.user_tags.items():
            if tag in extra_data.get("tags", []):
                hashes_found.append(hash_)
        return hashes_found

    def dict(self):
        return {"tags": self.user_tags}

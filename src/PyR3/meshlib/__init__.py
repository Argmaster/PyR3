# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import Iterable, List, Set, Tuple

from PyR3.construct.mp import ProjectComponent
from PyR3.meshlib.lib_obj.model_info import ModelInfoV1_0_0

from .lib_obj import LibraryObject, load


def get_meshlib_path_from_env() -> List[str]:
    ENV_MESHLIBPATH = os.environ.get("MESHLIBPATH", "").strip().split(";")[:-1]
    return ENV_MESHLIBPATH


def get_meshlib_path_from_file(file_path: str = "meshlib.path") -> List[str]:
    file_path: Path = Path(file_path)
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            PATHS = []
            for line in file.readlines():
                path = Path(line.strip()).resolve()
                if path.exists():
                    PATHS.append(str(path))
        return PATHS
    else:
        return []


class LibraryManager:

    PATH: List[Path]
    LIBS: List[LibraryObject]

    def __init__(self, lib_path: List[str]) -> None:
        self.set_path(lib_path)

    def set_path(self, lib_path: List[str]):
        """Changes value of PATH and performs library search on them.

        :param lib_path: List of paths to libraries/library containing folders.
        :type lib_path: List[str]
        """
        self.PATH = [Path(path).resolve() for path in lib_path]
        self._find_libs()

    def _find_libs(self):
        self.LIBS = []
        for sub_path in self.PATH:
            self.LIBS.extend(self._find_lib_files(sub_path))

    def _find_lib_files(self, path: Path) -> Iterable[LibraryObject]:
        libraries = []
        if path.is_dir():
            for glob_pattern in (
                str(path / "__lib__.yaml"),
                str(path / "*" / "__lib__.yaml"),
            ):
                for file_path in glob(glob_pattern):
                    library_object = load(file_path)
                    if library_object not in libraries:
                        libraries.append(library_object)
        elif path.is_file():
            libraries.append(load(path))
        return libraries

    def get_by_hash(self, hash_: str) -> ModelInfoV1_0_0:
        """Searches models contained in all libraries to find model with
        matching hash. If model is found, it is instantly returned, if no model
        is found, ValueError is being raised.

        :param hash_: hash value to look for.
        :type hash_: str
        :raises KeyError: raised if no matching model found.
        :return: model if found.
        :rtype: Optional[ModelInfoV1_0_0]
        """
        for library in self.LIBS:
            try:
                return library.match_hash(hash_)
            except KeyError:
                pass
        raise KeyError(f"Model with hash '{hash_}' not found.")

    def get_by_tag(
        self, tag: str
    ) -> List[Tuple[LibraryObject, ModelInfoV1_0_0]]:
        """Searches models contained in all libraries to find models with
        matching tag. Models found are appended to list, which is later
        returned. If no models is found, empty list is returned.

        :param tag: tag value to look for.
        :type tag: str
        :return: list of models found.
        :rtype: List[Tuple[LibraryObject, ModelInfoV1_0_0]]
        """
        models = []
        for library in self.LIBS:
            for mi in library.match_tag(tag):
                models.append((library, mi))
        return models

    @dataclass
    class Model_for_ProjectComponent:
        models: List[ModelInfoV1_0_0]

    def get_for_project_component(
        self, component: ProjectComponent
    ) -> List[ModelInfoV1_0_0]:
        """Find matching models for requirements contained in ProjectComponent
        object. Model(s) are always returned in list, regardles conditions
        resulting in founding them. When lookin for model, firstly attemt for
        finding one with matching hash is performed, if it succeeds, no further
        searching is done. If hash searching fails, tags are used. Only models
        with having all the tags from component.tags are contained in returned
        sequence.

        :param component: component requirements info
        :type component: ProjectComponent
        :return: list of matching ModelInfoV1_0_0 objects.
        :rtype: List[ModelInfoV1_0_0]
        """
        try:
            return [self.get_by_hash(component.hash)]
        except KeyError:
            pass
        return self.get_with_all_tags_matching(component.tags)

    def get_with_all_tags_matching(
        self, tags: List[str]
    ) -> List[ModelInfoV1_0_0]:
        """Searches for ModelInfo objects that has all the tags form `tags`
        variable in their tags set.

        :param tags: list of required tags.
        :type tags: List[str]
        :return: List of objects with all the tags present.
        :rtype: List[ModelInfoV1_0_0]
        """
        if len(tags) == 0:
            return []
        mi_list: List[ModelInfoV1_0_0] = self.get_by_tag(tags[0])
        mi_list_with_full_tag_match: List[str] = []
        for lib, mi in mi_list:
            model_tags: Set[str] = lib.get_all_tags_associated_with_model(mi)
            for tag in tags:
                if tag not in model_tags:
                    break
            else:
                mi_list_with_full_tag_match.append(mi)
        return mi_list_with_full_tag_match

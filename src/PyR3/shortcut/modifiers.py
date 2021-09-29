# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from operator import getitem
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import bpy

from PyR3.shortcut.context import Objects


class _Modifier(ABC):
    def apply(self, **extra_params):
        MODIFIER = self.master_object.modifiers.new(
            self.__class__.__qualname__, self._get_modifier_type()
        )
        self._set_modifier_params(MODIFIER, self.__class__.__dataclass_fields__.keys())
        if extra_params:
            self._set_modifier_extra_params(MODIFIER, extra_params)
        self._apply_modifier(MODIFIER.name, self.master_object)

    @abstractmethod
    def _get_modifier_type(self) -> str:
        ...

    def _set_modifier_params(self, modifier: bpy.types.Modifier, param_keys: List[str]):
        for param_name in param_keys:
            if hasattr(modifier, param_name):
                param_value = getattr(self, param_name)
                setattr(modifier, param_name, param_value)

    def _set_modifier_extra_params(
        self, modifier: bpy.types.Modifier, extra: Dict[str, Any]
    ):
        for param_name in extra.keys():
            if hasattr(modifier, param_name):
                param_value = getitem(extra, param_name)
                setattr(modifier, param_name, param_value)

    def _apply_modifier(
        self, modifier_name: bpy.types.Modifier, ob: bpy.types.Object
    ) -> None:
        Objects.select_only(ob)
        Objects.active = ob
        bpy.ops.object.modifier_apply(modifier=modifier_name)


@dataclass
class Boolean(_Modifier):
    """Boolean Modifier wrapper. For documentation over modifier parameters
    visit https://docs.blender.org/api/current/bpy.types.BooleanModifier.html
    """

    master_object: bpy.types.Object
    object: bpy.types.Object
    operation: str = "DIFFERENCE"
    solver: str = "EXACT"
    use_self: bool = False

    def _get_modifier_type(self):
        return "BOOLEAN"


@dataclass
class Array(_Modifier):
    """Array modifier wrapper. For documentation over modifier parameters
    visit https://docs.blender.org/api/current/bpy.types.ArrayModifier.html
    """

    master_object: bpy.types.Object
    constant_offset_displace: Tuple[float, float, float] = (0, 0, 0)
    count: int = 1
    use_relative_offset: bool = False
    use_constant_offset: bool = True

    def _get_modifier_type(self):
        return "ARRAY"


@dataclass
class Solidify(_Modifier):
    """Solidify modifier wrapper. For documentation over modifier parameters
    visit https://docs.blender.org/api/current/bpy.types.SolidifyModifier.html
    """

    master_object: bpy.types.Object
    thickness: float = 0.01
    offset: float = -1
    use_even_offset: bool = False
    use_quality_normals: bool = True

    def _get_modifier_type(self):
        return "SOLIDIFY"


@dataclass
class Bevel(_Modifier):
    """Solidify modifier wrapper. For documentation over modifier parameters
    visit https://docs.blender.org/api/current/bpy.types.BevelModifier.html
    """

    master_object: bpy.types.Object
    affect: str = "EDGES"
    offset_type: str = "OFFSET"
    width: float = 0.1
    segments: int = 1
    limit_method: str = "NONE"
    angle_limit: float = math.pi / 6
    use_clamp_overlap: bool = True

    def _get_modifier_type(self):
        return "BEVEL"

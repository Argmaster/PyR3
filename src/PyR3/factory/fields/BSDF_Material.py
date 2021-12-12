# -*- coding: utf-8 -*-


from operator import setitem
from typing import Any, Callable, Tuple

from PyR3.factory.fields.Sequence import HomotypeSequence

from .Color import Color
from .Number import Float
from .Struct import Struct

Color_T = Tuple[float, float, float, float]
Vector3D_T = Tuple[float, float, float]


class BSDF_Material(Struct):

    color: Color_T = Color(default="#FFFF")
    subsurface: float = Float(min=0.0, max=1.0, default=0.0)
    subsurfaceRadius: Vector3D_T = HomotypeSequence(
        Float(), length=3, default=(1.0, 0.2, 0.1)
    )
    subsurfaceColor: Color_T = Color(default="#FFFF")
    metallic: float = Float(min=0.0, max=1.0, default=0.0)
    specular: float = Float(min=0.0, max=1.0, default=0.5)
    specularTint: float = Float(min=0.0, max=1.0, default=0.5)
    roughness: float = Float(min=0.0, max=1.0, default=0.4)
    anisotropic: float = Float(min=0.0, max=1.0, default=0.0)
    anisotropicRotation: float = Float(min=0.0, max=1.0, default=0.0)
    sheen: float = Float(min=0.0, max=1.0, default=0.0)
    sheenTint: float = Float(min=0.0, max=1.0, default=0.5)
    clearcoat: float = Float(min=0.0, max=1.0, default=0.0)
    clearcoatRoughness: float = Float(min=0.0, max=1.0, default=0.03)
    IOR: float = Float(min=0.0, default=1.450)
    transmission: float = Float(min=0.0, max=1.0, default=0.0)
    transmissionRoughness: float = Float(min=0.0, max=1.0, default=0.0)
    emission: Color_T = Color(default="#0000")
    emissionStrength: float = Float(min=0.0, default=0.0)
    alpha: float = Float(min=0.0, max=1.0, default=1.0)

    def _get_container(self) -> Any:
        return dict()

    def _get_setter_function(self) -> Callable:
        return setitem

# -*- coding: utf-8 -*-


from typing import Tuple

from PyR3.factory.fields.Sequence import HomotypeSequence

from .Color import Color
from .Number import Float
from .Struct import Struct

Color_T = Tuple[float, float, float, float]
Vector3D_T = Tuple[float, float, float]


class BSDF_Material(Struct):

    color: Color_T = Color(default="#FFFF")
    subsurface: float = Float(min=0.0, max=1.0, default=0.0)
    subsurfaceRadius: Vector3D_T = HomotypeSequence(Float(), length=3)
    subsurfaceColor: Color_T = Color()
    metallic: float = Float(min=0.0, max=1.0)
    specular: float = Float(min=0.0, max=1.0)
    specularTint: float = Float(min=0.0, max=1.0)
    roughness: float = Float(min=0.0, max=1.0)
    anisotropic: float = Float(min=0.0, max=1.0)
    anisotropicRotation: float = Float(min=0.0, max=1.0)
    sheen: float = Float(min=0.0, max=1.0)
    sheenTint: float = Float(min=0.0, max=1.0)
    clearcoat: float = Float(min=0.0, max=1.0)
    clearcoatRoughness: float = Float(min=0.0, max=1.0)
    IOR: float = Float(min=0.0)
    transmission: float = Float(min=0.0, max=1.0)
    transmissionRoughness: float = Float(min=0.0, max=1.0)
    emission: Color_T = Color()
    emissionStrength: float = Float(min=0.0)
    alpha: float = Float(min=0.0, max=1.0)

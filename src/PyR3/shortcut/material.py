# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple

import bpy


def new_node_material(name: str = "material"):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    return material


Color_T = Tuple[float, float, float, float]


def update_BSDF_node(
    material: bpy.types.Material,
    color: Color_T = None,
    subsurface: float = None,
    subsurfaceRadius: tuple = None,
    subsurfaceColor: Color_T = None,
    metallic: float = None,
    specular: float = None,
    specularTint: float = None,
    roughness: float = None,
    anisotropic: float = None,
    anisotropicRotation: float = None,
    sheen: float = None,
    sheenTint: float = None,
    clearcoat: float = None,
    clearcoatRoughness: float = None,
    IOR: float = None,
    transmission: float = None,
    transmissionRoughness: float = None,
    emission: Color_T = None,
    emissionStrength: float = None,
    alpha: float = None,
) -> None:
    """Updates default values in Principled BSDF node of material.
    None params are ignored and doesn't modify node.

    :param material: Material to modify.
    :type material: bpy.types.Material
    :param color: Diffuse or metal surface color.
    :type color: Color_T, optional
    :param subsurface: Mix between diffuse and subsurface scattering. Rather than being a simple mix between Diffuse and Subsurface Scattering, it acts as a multiplier for the Subsurface Radius.
    :type subsurface: float, optional
    :param subsurfaceRadius: Average distance that light scatters below the surface. Higher radius gives a softer appearance, as light bleeds into shadows and through the object. The scattering distance is specified separately for the RGB channels, to render materials such as skin where red light scatters deeper. The X, Y and Z values are mapped to the R, G and B values, respectively.
    :type subsurfaceRadius: tuple, optional
    :param subsurfaceColor: Subsurface scattering base color.
    :type subsurfaceColor: Color_T, optional
    :param metallic: Blends between a non-metallic and metallic material model. A value of 1.0 gives a fully specular reflection tinted with the base color, without diffuse reflection or transmission. At 0.0 the material consists of a diffuse or transmissive base layer, with a specular reflection layer on top.
    :type metallic: float, optional
    :param specular: Amount of dielectric specular reflection. Specifies facing (along normal) reflectivity in the most common 0 - 8% range.
    :type specular: float, optional
    :param specularTint: Tints the facing specular reflection using the base color, while glancing reflection remains white.
    :type specularTint: float, optional
    :param roughness: Specifies microfacet roughness of the surface for diffuse and specular reflection.
    :type roughness: float, optional
    :param anisotropic: Amount of anisotropy for specular reflection. Higher values give elongated highlights along the tangent direction; negative values give highlights shaped perpendicular to the tangent direction.
    :type anisotropic: float, optional
    :param anisotropicRotation: Rotates the direction of anisotropy, with 1.0 going full circle.
    :type anisotropicRotation: float, optional
    :param sheen: Amount of soft velvet like reflection near edges, for simulating materials such as cloth.
    :type sheen: float, optional
    :param sheenTint: Mix between white and using base color for sheen reflection.
    :type sheenTint: float, optional
    :param clearcoat: Extra white specular layer on top of others. This is useful for materials like car paint and the like.
    :type clearcoat: float, optional
    :param clearcoatRoughness: Roughness of clearcoat specular.
    :type clearcoatRoughness: float, optional
    :param IOR: Index of refraction for transmission.
    :type IOR: float, optional
    :param transmission: Mix between fully opaque surface at zero and fully glass like transmission at one.
    :type transmission: float, optional
    :param transmissionRoughness: With GGX distribution controls roughness used for transmitted light.
    :type transmissionRoughness: float, optional
    :param emission: Light emission from the surface, like the Emission shader.
    :type emission: Color_T, optional
    :param emissionStrength: Strength of the emitted light. A value of 1.0 will ensure that the object in the image has the exact same color as the Emission Color, i.e. make it ‘shadeless’.
    :type emissionStrength: float, optional
    :param alpha: Controls the transparency of the surface, with 1.0 fully opaque. Usually linked to the Alpha output of an Image Texture node.
    :type alpha: float, optional
    :return: [description]
    :rtype: [type]
    """
    BSDF_node = material.node_tree.nodes["Principled BSDF"]
    if color is not None:
        BSDF_node.inputs[0].default_value = color
    if subsurface is not None:
        BSDF_node.inputs[1].default_value = subsurface
    if subsurfaceRadius is not None:
        BSDF_node.inputs[2].default_value[0] = subsurfaceRadius[0]
        BSDF_node.inputs[2].default_value[1] = subsurfaceRadius[1]
        BSDF_node.inputs[2].default_value[2] = subsurfaceRadius[2]
    if subsurfaceColor is not None:
        BSDF_node.inputs[3].default_value = color
    if metallic is not None:
        BSDF_node.inputs[4].default_value = metallic
    if specular is not None:
        BSDF_node.inputs[5].default_value = specular
    if specularTint is not None:
        BSDF_node.inputs[6].default_value = specularTint
    if roughness is not None:
        BSDF_node.inputs[7].default_value = roughness
    if anisotropic is not None:
        BSDF_node.inputs[8].default_value = anisotropic
    if anisotropicRotation is not None:
        BSDF_node.inputs[9].default_value = anisotropicRotation
    if sheen is not None:
        BSDF_node.inputs[10].default_value = sheen
    if sheenTint is not None:
        BSDF_node.inputs[11].default_value = sheenTint
    if clearcoat is not None:
        BSDF_node.inputs[12].default_value = clearcoat
    if clearcoatRoughness is not None:
        BSDF_node.inputs[13].default_value = clearcoatRoughness
    if IOR is not None:
        BSDF_node.inputs[14].default_value = IOR
    if transmission is not None:
        BSDF_node.inputs[15].default_value = transmission
    if transmissionRoughness is not None:
        BSDF_node.inputs[16].default_value = transmissionRoughness
    if emission is not None:
        BSDF_node.inputs[17].default_value = color
    if emissionStrength is not None:
        BSDF_node.inputs[18].default_value = emissionStrength
    if alpha is not None:
        BSDF_node.inputs[19].default_value = alpha
    return BSDF_node.material

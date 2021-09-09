import bpy


class Transform:
        @staticmethod
        def apply(location: bool = True, rotation: bool = True, scale: bool = True):
            """Apply current transformation of object to it.

            Args:
                location (bool, optional): Flag specifying wheather to apply transform or not. Defaults to True.
                rotation (bool, optional): Flag specifying wheather to apply rotation or not. Defaults to True.
                scale (bool, optional): Flag specifying wheather to apply scale or not. Defaults to True.
            """
            bpy.ops.object.transform_apply(
                location=location, rotation=rotation, scale=scale
            )

        @staticmethod
        def transform(
            rotation: tuple = (0, 0, 0),
            translation: tuple = (0, 0, 0),
            scale: tuple = (0, 0, 0),
        ):
            """Function that can be used to transform object by vector in both Edit and Object mode.

            Args:
                rotation (tuple, optional): vector of (float, float, float). Defaults to (0, 0, 0).
                translation (tuple, optional): vector of (float, float, float). Defaults to (0, 0, 0).
                scale (tuple, optional): vector of (float, float, float). Defaults to (0, 0, 0).
            """
            Blender.Transform.scale(scale)
            Blender.Transform.rotateX(rotation[0])
            Blender.Transform.rotateY(rotation[1])
            Blender.Transform.rotateZ(rotation[2])
            Blender.Transform.translate(translation)

        @staticmethod
        def translate(
            xyz: Tuple[float, float, float] = (0.0, 0.0, 0.0),
            orient_type: str = "GLOBAL",
            orient_matrix: tuple = ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type: str = "GLOBAL",
            constraint_axis: tuple = (False, False, False),
            mirror: bool = True,
            use_proportional_edit: bool = False,
            proportional_edit_falloff: str = "SMOOTH",
            proportional_size: float = 1,
            use_proportional_connected: bool = False,
            use_proportional_projected: bool = False,
            release_confirm: bool = True,
            **kwargs,
        ) -> set:
            """Apply translate transform for both object and edit mode
            Args:
                xyz (Tuple[float, float, float], optional): translation vector. Defaults to (0.0, 0.0, 0.0).
                orient_type (str, optional): ["GLOBAL", "LOCAL", "NORMAL", "GIMBAL", "VIEW", "CURSOR"] Defaults to "GLOBAL".
                orient_matrix_type (str, optional): ["GLOBAL", "LOCAL", "NORMAL", "GIMBAL", "VIEW", "CURSOR"] Defaults to "GLOBAL".
            """
            return bpy.ops.transform.translate(
                value=xyz,
                orient_type=orient_type,
                orient_matrix=orient_matrix,
                orient_matrix_type=orient_matrix_type,
                constraint_axis=constraint_axis,
                mirror=mirror,
                use_proportional_edit=use_proportional_edit,
                proportional_edit_falloff=proportional_edit_falloff,
                proportional_size=proportional_size,
                use_proportional_connected=use_proportional_connected,
                use_proportional_projected=use_proportional_projected,
                release_confirm=release_confirm,
                **kwargs,
            )

        @staticmethod
        def rotate(
            value: float = 0,
            orient_axis: str = "X",
            orient_type: str = "GLOBAL",
            orient_matrix: tuple = ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type: str = "GLOBAL",
            constraint_axis: tuple = (False, False, False),
            mirror: bool = True,
            use_proportional_edit: bool = False,
            proportional_edit_falloff: str = "SMOOTH",
            proportional_size: float = 1,
            use_proportional_connected: bool = False,
            use_proportional_projected: bool = False,
            release_confirm: bool = True,
            center_override=(0.0, 0.0, 0.0),
            **kwargs,
        ) -> set:
            """Apply rotation transform to object. It works both in Object and Edit mode.
            If center_override is None it wont be contained in end rotation so center wont be overriden.

            Args:
                value (float, optional): Angle in radians. Defaults to 0.
                orient_axis (str, optional): . Defaults to "X".
                orient_type (str, optional): ["GLOBAL", "LOCAL", "NORMAL", "GIMBAL", "VIEW", "CURSOR"] Defaults to "GLOBAL".
                orient_matrix_type (str, optional): ["GLOBAL", "LOCAL", "NORMAL", "GIMBAL", "VIEW", "CURSOR"] Defaults to "GLOBAL".
            """
            if center_override is not None:
                kwargs["center_override"] = center_override
            return bpy.ops.transform.rotate(
                value=value,
                orient_axis=orient_axis,
                orient_type=orient_type,
                orient_matrix=orient_matrix,
                orient_matrix_type=orient_matrix_type,
                constraint_axis=constraint_axis,
                mirror=mirror,
                use_proportional_edit=use_proportional_edit,
                proportional_edit_falloff=proportional_edit_falloff,
                proportional_size=proportional_size,
                use_proportional_connected=use_proportional_connected,
                use_proportional_projected=use_proportional_projected,
                release_confirm=release_confirm,
                **kwargs,
            )

        @staticmethod
        def rotateX(
            value: float, center_override: tuple = (0.0, 0.0, 0.0), **kwargs
        ) -> set:
            """Rotate currently selected object in predefined axis. It works both in Object and Edit mode.
            If center_override is None it wont be contained in end rotation so center wont be overriden.

            Args:
                value (float): rotation value
                center_override (tuple, optional): Overwriting of rotation center. Defaults to (0.0, 0.0, 0.0).

            Returns:
                set: set containing operation result.
            """
            return Blender.Transform.rotate(
                value,
                orient_axis="X",
                constraint_axis=(True, False, False),
                center_override=center_override,
                **kwargs,
            )

        @staticmethod
        def rotateY(
            value: float, center_override: tuple = (0.0, 0.0, 0.0), **kwargs
        ) -> set:
            """Rotate currently selected object in predefined axis. It works both in Object and Edit mode.
            If center_override is None it wont be contained in end rotation so center wont be overriden.

            Args:
                value (float): rotation value
                center_override (tuple, optional): Overwriting of rotation center. Defaults to (0.0, 0.0, 0.0).

            Returns:
                set: set containing operation result.
            """
            return Blender.Transform.rotate(
                value,
                orient_axis="Y",
                constraint_axis=(False, True, False),
                center_override=center_override,
                **kwargs,
            )

        @staticmethod
        def rotateZ(
            value: float, center_override: tuple = (0.0, 0.0, 0.0), **kwargs
        ) -> set:
            """Rotate currently selected object in predefined axis. It works both in Object and Edit mode.
            If center_override is None it wont be contained in end rotation so center wont be overriden.

            Args:
                value (float): rotation value
                center_override (tuple, optional): Overwriting of rotation center. Defaults to (0.0, 0.0, 0.0).

            Returns:
                set: set containing operation result.
            """
            return Blender.Transform.rotate(
                value,
                orient_axis="Z",
                constraint_axis=(False, False, True),
                center_override=center_override,
                **kwargs,
            )

        @staticmethod
        def scale(
            xyz: tuple = (1, 1, 1),
            orient_type: str = "GLOBAL",
            orient_matrix: tuple = ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type: str = "GLOBAL",
            constraint_axis: Tuple[bool, bool, bool] = (False, False, False),
            mirror: bool = True,
            use_proportional_edit: bool = False,
            proportional_edit_falloff: str = "SMOOTH",
            proportional_size: float = 1,
            use_proportional_connected: bool = False,
            use_proportional_projected: bool = False,
            release_confirm: bool = True,
            **kwargs,
        ) -> set:
            """Scale currently selected object. It works both in object and edit mode.

            Args:
                xyz (tuple, optional): Scalin in each axis. Defaults to (1, 1, 1).
                orient_type (str, optional): ["GLOBAL", "LOCAL", "NORMAL", "GIMBAL", "VIEW", "CURSOR"]. Defaults to "GLOBAL".
                orient_matrix (tuple, optional): . Defaults to ((1, 0, 0), (0, 1, 0), (0, 0, 1)).
                orient_matrix_type (str, optional): . Defaults to "GLOBAL".
                constraint_axis (Tuple[bool, bool, bool], optional): . Defaults to (False, False, False).
                mirror (bool, optional): . Defaults to True.
                use_proportional_edit (bool, optional): . Defaults to False.
                proportional_edit_falloff (str, optional): . Defaults to "SMOOTH".
                proportional_size (float, optional): . Defaults to 1.
                use_proportional_connected (bool, optional): . Defaults to False.
                use_proportional_projected (bool, optional): . Defaults to False.
                release_confirm (bool, optional): . Defaults to True.
            """
            return bpy.ops.transform.resize(
                value=xyz,
                orient_type=orient_type,
                orient_matrix=orient_matrix,
                orient_matrix_type=orient_matrix_type,
                constraint_axis=constraint_axis,
                mirror=mirror,
                use_proportional_edit=use_proportional_edit,
                proportional_edit_falloff=proportional_edit_falloff,
                proportional_size=proportional_size,
                use_proportional_connected=use_proportional_connected,
                use_proportional_projected=use_proportional_projected,
                release_confirm=release_confirm,
                **kwargs,
            )

        resize = scale
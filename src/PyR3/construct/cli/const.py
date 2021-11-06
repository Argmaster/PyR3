# -*- coding: utf-8 -*-

from typing import Any

from rich.console import Console


class ConsoleWrapperType:
    def __init__(self) -> None:
        self.__dict__["console"] = Console()

    def disable_rich(self) -> None:
        self.__dict__["console"] = Console(
            color_system=None,
            highlight=False,
            highlighter=None,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self.console, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self.console, name, value)


CONSOLE = ConsoleWrapperType()


class EXIT_CODE:
    MESHPROJECT_FILE_NOT_FOUND = 2
    COMPONENT_WITH_SYMBOL_EXISTS = 345
    MESHPROJECT_INVALID_FIELD_VALUE = 347
    MESHPROJECT_FILE_INVALID_YAML_SYNTAX = 348
    FILE_EXISTS = 349

# -*- coding: utf-8 -*-
from typing import Any

import click
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


CONSOLE: Console = ConsoleWrapperType()


@click.group()
@click.option(
    "--no-rich",
    is_flag=True,
    help="Disable rich output (color tags, formatting).",
)
def common_main(no_rich: bool):
    if no_rich:
        CONSOLE.disable_rich()

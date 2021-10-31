# -*- coding: utf-8 -*-
import re
from pathlib import Path
from typing import ClassVar

import yaml
from pydantic import BaseModel, validator


class PlaceFile:

    file_path: Path
    project_name: str
    units: str
    note: str

    REGEX: ClassVar[re.Pattern] = re.compile(
        (
            r"(?P<HEADER>.*?)"
            r" RefDes        Footprint         Side    Loc X    Loc Y   Rot  Glue X   Glue Y   Glu Dia  Technology  Pins\s+"
            r"--------  --------------------  ------  -------  -------  ---  -------  -------  -------  ----------  ----\s+"
            r"(?P<TABLE>.*)"
        ),
        re.DOTALL,
    )

    @staticmethod
    def load(path: Path):
        with path.open("r", encoding="utf-8") as file:
            buffer = file.read()
        return PlaceFile(path, buffer)

    def __init__(self, file_path: Path, raw: str) -> None:
        self.file_path = file_path
        self._process_place(raw)

    def _process_place(self, raw: str):
        if (match := self.REGEX.match(raw)) is None:
            raise RuntimeError(f"Failed to parse '{self.file_path}' Place file.")
        groupdict = match.groupdict()
        self._process_header(groupdict.get("HEADER"))
        self._process_table(groupdict.get("TABLE"))

    def _process_header(self, header_string: str):
        header: dict = yaml.safe_load(header_string)
        self.project_name = header.get("Project")
        if "\n" in self.project_name:
            self.project_name = self.project_name.split("\n")[0].strip()
        self.units = header.get("Units")
        self.note = header.get("Note")

    def _process_table(self, table_string: str):
        self.component_list = []
        for row in table_string.strip().split("\n"):
            values = row.split()
            component = PlaceComponent(
                symbol=values[0],
                footprint=values[1],
                side=values[2],
                x=values[3],
                y=values[4],
                rotation=values[5],
                glue_x=values[6],
                glue_y=values[7],
                glu_dia=values[8],
                technology=values[9],
                pin_count=values[10],
            )
            self.component_list.append(component)

    def dict(self):
        return {
            "project_name": self.project_name,
            "units": self.units,
            "component_list": [component.dict() for component in self.component_list],
        }

    def __str__(self) -> str:
        return f"Place[{self.project_name} {len(self.component_list)} components]"


class PlaceComponent(BaseModel):

    symbol: str
    footprint: str
    side: str
    x: float
    y: float
    rotation: float
    glue_x: float
    glue_y: float
    glu_dia: float
    technology: str
    pin_count: int

    @validator(
        "x",
        "y",
        "rotation",
        "glue_x",
        "glue_y",
        "glu_dia",
        pre=True,
    )
    def _parse_float(value: str):
        return float(value)

    @validator("pin_count", pre=True)
    def _parse_int(value: str):
        return int(value)

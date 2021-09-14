# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any


class Field(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def digest(self, value: Any) -> None:
        ...


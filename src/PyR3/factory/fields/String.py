# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from .Field import Field


class String(Field):
    """String factory field. You can specify length and default for it.
    Its value is always a string.

    :param default: Default value, used if no value is provided.
        If None, exception will be raised if no value will be given, defaults to None
    :type default: str, optional
    :param min_length: Minimal length of string. Exception will be raised
        if requirement will not be fullfiled. Defaults to None
    :type min_length: int, optional
    :param max_length: Minimal length of string. Exception will be raised
        if requirement will not be fullfiled. Defaults to None
    :type max_length: int, optional
    """

    def __init__(
        self, *, default: str = None, min_length: int = None, max_length: int = None
    ) -> None:
        self.default = default
        self.min_length = min_length
        self.max_length = max_length

    def digest(self, value: str = None) -> str:
        """Consumes value and returns cleaned string.
        Raises exception if requirements for string
        format are not met.

        :param value: value to consume, defaults to None
        :type value: str, optional
        :return: cleaned string.
        :rtype: str
        """
        if value is None:
            return self._get_default()
        else:
            string = str(value)
            self._check_conditions(string)
            return string

    def _check_conditions(self, string: str):
        if self.min_length is not None:
            if not (self.min_length <= len(string)):
                raise ValueError(
                    f"String for {self._trace_location()} is too short ({len(string)}, min length: {self.min_length})"
                )
        if self.max_length is not None:
            if not (len(string) <= self.max_length):
                raise ValueError(
                    f"String for {self._trace_location()} is too long ({len(string)}, min length: {self.max_length})"
                )


class Regex(String):
    """String field with possibility to use regular expression
    to check if string format is valid.

    :param pattern: Regular expression patter. String will be automatically compiled.
    :type pattern: re.Pattern or str
    :param default: [description], defaults to None
    :type default: str, optional
    :param flags: regular expression flags, from re module, defaults to 0
    :type flags: int, optional
    :raises TypeError: if pattern is neither str or re.Pattern.
    """

    _pattern: re.Pattern

    def __init__(
        self, pattern: re.Pattern | str, *, default: str = None, flags: int = 0
    ) -> None:
        if isinstance(pattern, str):
            self._pattern = re.compile(pattern, flags=flags)
        elif isinstance(pattern, re.Pattern):
            self._pattern = pattern
        else:
            raise TypeError(f"Invalid type of pattern parameter: {type(pattern)}")
        self.default = default

    def _check_conditions(self, string: str):
        if not self._pattern.fullmatch(string):
            raise ValueError(
                f"Value '{string}' doesn't match pattern '{self._pattern.pattern}' of field {self._trace_location()}"
            )

# -*- coding: utf-8 -*-
from __future__ import annotations
from re import I

from unittest import TestCase, main

from PyR3.contrib.factories.CapacitorCase import CapacitorCase
from PyR3.shortcut.context import cleanScene
from PyR3.shortcut.io import export_blend


class TestCapacitorCylinder(TestCase):
    def test_instantiate(self):
        cleanScene()
        renderer = CapacitorCase({"height": "3mm", "radius": "1mm"})
        renderer.render()
        export_blend("")


if __name__ == "__main__":
    main()

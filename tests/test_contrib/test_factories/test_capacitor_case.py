# -*- coding: utf-8 -*-
from __future__ import annotations
from re import I

from unittest import TestCase, main

from PyR3.contrib.factories.CapacitorCase import CapacitorCase
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_blend


class TestCapacitorCylinder(TestCase):
    def test_instantiate(self):
        wipeScenes()
        renderer = CapacitorCase({"height": "3m", "radius": "1m"})
        renderer.render()
        export_blend(
            filepath="./tests/.temp/TestCapacitorCylinder_test_instantiate.blend"
        )


if __name__ == "__main__":
    main()

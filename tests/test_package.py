# -*- coding: utf-8 -*-
from __future__ import annotations
from unittest import TestCase, main


class Test(TestCase):
    def test_import_bpy(self):
        import bpy

        bpy.context
        bpy.app


if __name__ == "__main__":
    main()

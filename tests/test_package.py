# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase


class Test(TestCase):
    def test_import_bpy(self):
        import bpy

        bpy.context
        bpy.app

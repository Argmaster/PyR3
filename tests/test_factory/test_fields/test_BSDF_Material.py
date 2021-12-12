# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PyR3.factory.fields.BSDF_Material import BSDF_Material


class Test_BSDF_Material(TestCase):
    def test_use_defaults_only(self):
        material = BSDF_Material().digest({})
        self.assertIsInstance(material, dict)
        self.assertTrue(material)

    def test_use_partially_custom(self):
        material = BSDF_Material().digest(
            {
                "metallic": 0.833,
                "color": "#AC345F86",
            }
        )
        self.assertIsInstance(material, dict)
        self.assertTrue(material)
        self.assertEqual(
            material["color"],
            (172, 52, 95, 134),
        )
        self.assertEqual(material["metallic"], 0.833)


if __name__ == "__main__":
    main()

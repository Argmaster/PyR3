# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from PyR3.meshlib.lib_obj.usertags import UserTags, dump, load

from .test_lib_info import LIB_FILE_PATH

LIB_FILE_PATH
DIR = Path(__file__).parent
USER_TAGS_FILE_PATH = LIB_FILE_PATH.parent / "__user__.yaml"


class TestUserTags(TestCase):
    def test_load_UserTags_object(self):
        user_tags_ob = load(USER_TAGS_FILE_PATH)
        self.assertIsInstance(user_tags_ob, UserTags)

    def test_dump_UserTags_object(self):
        user_tags_ob = load(USER_TAGS_FILE_PATH)
        dump(user_tags_ob, USER_TAGS_FILE_PATH)

    def test_get_extra_tags(self):
        user_tags_ob = load(USER_TAGS_FILE_PATH)
        extra = user_tags_ob.get_extra_tags("e+kOrn6hL4tcJIHHwYWNLTbhzzY=")
        self.assertTrue(len(extra) == 2)
        self.assertTrue(set(extra) == {"UserCustomTag", "UserCustomTag1"})

    def test_get_hash_with_tag(self):
        user_tags_ob = load(USER_TAGS_FILE_PATH)
        hashes = user_tags_ob.get_hash_with_tag("UserCustomTag")
        self.assertTrue(len(hashes), 2)
        hashes = user_tags_ob.get_hash_with_tag("UserCustomTag1")
        self.assertTrue(len(hashes), 1)

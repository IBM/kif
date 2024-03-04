# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .tests import kif_EmptyStoreTestCase


class TestStoreDescriptors(kif_EmptyStoreTestCase):

    def test_get_descriptor(self):
        self.sanity_check_get_descriptor(self.new_Store())

    def test_get_item_descriptor(self):
        self.sanity_check_get_item_descriptor(self.new_Store())

    def test_get_property_descriptor(self):
        self.sanity_check_get_property_descriptor(self.new_Store())

    def test_get_lexeme_descriptor(self):
        self.sanity_check_get_lexeme_descriptor(self.new_Store())


if __name__ == '__main__':
    TestStoreDescriptors.main()

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store

from .tests import kif_StoreTestCase, main


class TestStoreDescriptors(kif_StoreTestCase):

    def test_get_item_descriptor(self):
        self.sanity_check_get_item_descriptor(Store('empty'))

    def test_get_property_descriptor(self):
        self.sanity_check_get_property_descriptor(Store('empty'))

    def test_get_lexeme_descriptor(self):
        self.sanity_check_get_lexeme_descriptor(Store('empty'))


if __name__ == '__main__':
    main()

# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .tests import EmptyStoreTestCase


class TestStoreABC_Descriptors(EmptyStoreTestCase):

    def test_get_descriptor(self) -> None:
        self.sanity_check_get_descriptor(self.new_Store())

    def test_get_item_descriptor(self) -> None:
        self.sanity_check_get_item_descriptor(self.new_Store())

    def test_get_property_descriptor(self) -> None:
        self.sanity_check_get_property_descriptor(self.new_Store())

    def test_get_lexeme_descriptor(self) -> None:
        self.sanity_check_get_lexeme_descriptor(self.new_Store())


if __name__ == '__main__':
    TestStoreABC_Descriptors.main()

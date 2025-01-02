# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json

from kif_lib import Quantity

from ..tests import TestCase


class Test(TestCase):

    def assert_to_json(self, obj, data) -> None:
        self.assertEqual(obj.to_json(), json.dumps(data))

    def test_quantity_to_json(self) -> None:
        self.assert_to_json(Quantity(1), {
            'class': 'Quantity',
            'args': ['1', None, None, None],
        })


if __name__ == '__main__':
    Test.main()

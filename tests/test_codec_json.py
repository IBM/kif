# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import json

from kif_lib import Quantity

from .tests import TestCase


class TestCodecJSON(TestCase):

    def assert_to_json(self, obj, data) -> None:
        self.assertEqual(obj.to_json(), json.dumps(data))

    def test_quantity_to_json(self) -> None:
        self.assert_to_json(Quantity(1), {
            'class': 'Quantity',
            'args': ['1', None, None, None],
        })


if __name__ == '__main__':
    TestCodecJSON.main()

# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, NoValueSnak, Property, String

from .tests import kif_TestCase


class TestModelSnakNoValueSnak(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, NoValueSnak, 0)
        self.assertRaises(TypeError, NoValueSnak, 'abc')
        self.assertRaises(TypeError, NoValueSnak, String('abc'))
        self.assert_no_value_snak(
            NoValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_no_value_snak(
            NoValueSnak(Property('abc')), Property('abc'))


if __name__ == '__main__':
    TestModelSnakNoValueSnak.main()

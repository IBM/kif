# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, Item, Property, Quantity, String, ValueSnak

from .tests import kif_TestCase


class TestValueSnak(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, ValueSnak, 0, 0)
        self.assertRaises(TypeError, ValueSnak, 'abc', 'abc')
        self.assertRaises(TypeError, ValueSnak, Property('abc'), {})
        self.assertRaises(TypeError, ValueSnak, String('abc'), [])
        self.assert_value_snak(
            ValueSnak(Property('abc'), IRI('abc')),
            Property(IRI('abc')), IRI('abc'))
        self.assert_value_snak(
            ValueSnak(Property('abc'), String('abc')),
            Property(IRI('abc')), String('abc'))
        self.assert_value_snak(
            ValueSnak(Property('abc'), Property('abc')),
            Property(IRI('abc')), Property('abc'))
        self.assert_value_snak(
            ValueSnak(Property('abc'), Item('abc')),
            Property(IRI('abc')), Item('abc'))
        self.assert_value_snak(
            ValueSnak(Property('abc'), .5),
            Property('abc'), Quantity(.5))
        self.assert_value_snak(
            ValueSnak(Property('abc'), 8),
            Property('abc'), Quantity(8))
        self.assert_value_snak(
            ValueSnak(Property('abc'), 'x'),
            Property('abc'), String('x'))


if __name__ == '__main__':
    TestValueSnak.main()

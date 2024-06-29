# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, Item, Property, Quantity, String, ValueSnak

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test__init__(self):
        # bad argument
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            ValueSnak, 0, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce dict into IRI',
            ValueSnak, dict(), 0)
        self.assert_raises_bad_argument(
            TypeError, 2, None,
            'cannot coerce dict into Value', ValueSnak, 'x', dict())
        # good argument
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
    Test.main()

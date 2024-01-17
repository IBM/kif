# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, Property, SomeValueSnak, String

from .tests import kif_TestCase, main


class TestModelSomeValueSnak(kif_TestCase):

    def test__init__(self):
        self.assertRaises(TypeError, SomeValueSnak, 0)
        self.assertRaises(TypeError, SomeValueSnak, 'abc')
        self.assertRaises(TypeError, SomeValueSnak, String('abc'))
        self.assert_some_value_snak(
            SomeValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_some_value_snak(
            SomeValueSnak(Property('abc')), Property('abc'))


if __name__ == '__main__':
    main()

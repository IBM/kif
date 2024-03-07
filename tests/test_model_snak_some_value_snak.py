# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, Property, SomeValueSnak, String

from .tests import kif_TestCase


class TestModelSnakSomeValueSnak(kif_TestCase):

    def test__init__(self):
        # bad argument
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected Property, got int',
            SomeValueSnak, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected Property, got str',
            SomeValueSnak, 'abc')
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'expected Property, got String',
            SomeValueSnak, String('abc'))
        # good argument
        self.assert_some_value_snak(
            SomeValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_some_value_snak(
            SomeValueSnak(Property('abc')), Property('abc'))


if __name__ == '__main__':
    TestModelSnakSomeValueSnak.main()

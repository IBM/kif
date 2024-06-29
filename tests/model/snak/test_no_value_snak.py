# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, NoValueSnak, Property, String

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test__init__(self):
        # bad argument
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            NoValueSnak, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce dict into IRI',
            NoValueSnak, {})
        # good argument
        self.assert_no_value_snak(
            NoValueSnak(IRI('abc')), Property(IRI('abc')))
        self.assert_no_value_snak(
            NoValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_no_value_snak(
            NoValueSnak(String('abc')), Property('abc'))
        self.assert_no_value_snak(
            NoValueSnak('abc'), Property('abc'))


if __name__ == '__main__':
    Test.main()

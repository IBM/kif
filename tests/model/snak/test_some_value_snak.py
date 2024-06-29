# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef

from kif_lib import IRI, Property, SomeValueSnak, String

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test__init__(self):
        # bad argument
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce int into IRI',
            SomeValueSnak, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None, 'cannot coerce dict into IRI',
            SomeValueSnak, dict())
        # good argument
        self.assert_some_value_snak(
            SomeValueSnak(IRI('abc')), Property(IRI('abc')))
        self.assert_some_value_snak(
            SomeValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_some_value_snak(
            SomeValueSnak(String('abc')), Property('abc'))
        self.assert_some_value_snak(
            SomeValueSnak(URIRef('abc')), Property('abc'))
        self.assert_some_value_snak(
            SomeValueSnak('abc'), Property('abc'))


if __name__ == '__main__':
    Test.main()

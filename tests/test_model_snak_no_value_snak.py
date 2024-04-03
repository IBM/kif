# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import URIRef

from kif_lib import IRI, NoValueSnak, Property, String

from .tests import kif_TestCase


class TestModelSnakNoValueSnak(kif_TestCase):

    def test__init__(self):
        # bad argument
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or Property or String or URIRef or str, got int',
            NoValueSnak, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, None,
            'expected IRI or Property or String or URIRef or str, got dict',
            NoValueSnak, dict())
        # good argument
        self.assert_no_value_snak(
            NoValueSnak(IRI('abc')), Property(IRI('abc')))
        self.assert_no_value_snak(
            NoValueSnak(Property('abc')), Property(IRI('abc')))
        self.assert_no_value_snak(
            NoValueSnak(String('abc')), Property('abc'))
        self.assert_no_value_snak(
            NoValueSnak(URIRef('abc')), Property('abc'))
        self.assert_no_value_snak(
            NoValueSnak('abc'), Property('abc'))


if __name__ == '__main__':
    TestModelSnakNoValueSnak.main()

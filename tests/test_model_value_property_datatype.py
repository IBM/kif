# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Property, PropertyDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValuePropertyDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_property_datatype(
            PropertyDatatype._from_rdflib(WIKIBASE.WikibaseProperty))

    def test__to_rdflib(self):
        self.assertEqual(
            PropertyDatatype._to_rdflib(), WIKIBASE.WikibaseProperty)

    def test_from_value_class(self):
        self.assert_property_datatype(Datatype.from_value_class(Property))

    def test_to_value_class(self):
        self.assertIs(PropertyDatatype().to_value_class(), Property)


if __name__ == '__main__':
    TestModelValuePropertyDatatype.main()

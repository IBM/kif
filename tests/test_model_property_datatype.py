# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Property, PropertyDatatype

from .tests import kif_TestCase, main


class TestModelPropertyDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.property, Property.datatype)
        self.assertEqual(Datatype.property, PropertyDatatype())

    def test__from_rdflib(self):
        self.assert_property_datatype(
            PropertyDatatype._from_rdflib(NS.WIKIBASE.WikibaseProperty))

    def test__to_rdflib(self):
        self.assertEqual(
            PropertyDatatype._to_rdflib(), NS.WIKIBASE.WikibaseProperty)


if __name__ == '__main__':
    main()

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, Quantity, QuantityDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueQuantityDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_quantity_datatype(
            QuantityDatatype._from_rdflib(WIKIBASE.Quantity))

    def test__to_rdflib(self):
        self.assertEqual(QuantityDatatype._to_rdflib(), WIKIBASE.Quantity)

    def test_from_value_class(self):
        self.assert_quantity_datatype(Datatype.from_value_class(Quantity))

    def test_to_value_class(self):
        self.assertIs(QuantityDatatype().to_value_class(), Quantity)


if __name__ == '__main__':
    TestModelValueQuantityDatatype.main()

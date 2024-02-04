# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, Quantity, QuantityDatatype

from .tests import kif_TestCase, main


class TestModelQuantityDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.quantity, Quantity.datatype)
        self.assertEqual(Datatype.quantity, QuantityDatatype())

    def test__from_rdflib(self):
        self.assert_quantity_datatype(
            QuantityDatatype._from_rdflib(NS.WIKIBASE.Quantity))

    def test__to_rdflib(self):
        self.assertEqual(
            QuantityDatatype._to_rdflib(), NS.WIKIBASE.Quantity)


if __name__ == '__main__':
    main()

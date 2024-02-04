# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, ExternalId, ExternalIdDatatype

from .tests import kif_TestCase, main


class TestModelExternalIdDatatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.external_id, ExternalId.datatype)
        self.assertEqual(Datatype.external_id, ExternalIdDatatype())

    def test__from_rdflib(self):
        self.assert_external_id_datatype(
            ExternalIdDatatype._from_rdflib(NS.WIKIBASE.ExternalId))

    def test__to_rdflib(self):
        self.assertEqual(
            ExternalIdDatatype._to_rdflib(), NS.WIKIBASE.ExternalId)


if __name__ == '__main__':
    main()

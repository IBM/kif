# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import ExternalId, ExternalIdDatatype

from .tests import kif_TestCase, main


class TestModelExternalIdDatatype(kif_TestCase):

    def test_value_class(self):
        self.assert_datatype_value_class(
            ExternalIdDatatype, ExternalId, 'external_id')

    def test__from_rdflib(self):
        self.assert_external_id_datatype(
            ExternalIdDatatype._from_rdflib(NS.WIKIBASE.ExternalId))

    def test__to_rdflib(self):
        self.assertEqual(
            ExternalIdDatatype._to_rdflib(), NS.WIKIBASE.ExternalId)


if __name__ == '__main__':
    main()

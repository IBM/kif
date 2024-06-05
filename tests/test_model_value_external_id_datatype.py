# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import ExternalIdDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueExternalIdDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_external_id_datatype(
            ExternalIdDatatype._from_rdflib(WIKIBASE.ExternalId))

    def test__to_rdflib(self):
        self.assertEqual(
            ExternalIdDatatype._to_rdflib(), WIKIBASE.ExternalId)


if __name__ == '__main__':
    TestModelValueExternalIdDatatype.main()

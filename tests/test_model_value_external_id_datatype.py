# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Datatype, ExternalId, ExternalIdDatatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueExternalIdDatatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_external_id_datatype(
            ExternalIdDatatype._from_rdflib(WIKIBASE.ExternalId))

    def test__to_rdflib(self):
        self.assertEqual(
            ExternalIdDatatype._to_rdflib(), WIKIBASE.ExternalId)

    def test_from_value_class(self):
        self.assert_external_id_datatype(Datatype.from_value_class(ExternalId))

    def test_to_value_class(self):
        self.assertIs(ExternalIdDatatype().to_value_class(), ExternalId)


if __name__ == '__main__':
    TestModelValueExternalIdDatatype.main()

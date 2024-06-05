# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI_Datatype
from kif_lib.namespace import WIKIBASE

from .tests import kif_TestCase


class TestModelValueIRI_Datatype(kif_TestCase):

    def test__from_rdflib(self):
        self.assert_iri_datatype(IRI_Datatype._from_rdflib(WIKIBASE.Url))

    def test__to_rdflib(self):
        self.assertEqual(IRI_Datatype._to_rdflib(), WIKIBASE.Url)


if __name__ == '__main__':
    TestModelValueIRI_Datatype.main()

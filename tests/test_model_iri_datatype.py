# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import kif_lib.namespace as NS
from kif_lib import Datatype, IRI, IRI_Datatype

from .tests import kif_TestCase, main


class TestModelIRI_Datatype(kif_TestCase):

    def test_sanity(self):
        self.assertIs(Datatype.iri, IRI.datatype)
        self.assertEqual(Datatype.iri, IRI_Datatype())

    def test__from_rdflib(self):
        self.assert_iri_datatype(IRI_Datatype._from_rdflib(NS.WIKIBASE.Url))

    def test__to_rdflib(self):
        self.assertEqual(IRI_Datatype._to_rdflib(), NS.WIKIBASE.Url)


if __name__ == '__main__':
    main()

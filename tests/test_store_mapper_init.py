# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Store
from kif_lib.store.mapper import SPARQL_MapperStore
from kif_lib.store.sparql_mapping import SPARQL_Mapping

from .tests import kif_StoreTestCase


class TestStoreMapper_Init(kif_StoreTestCase):

    def test__init__(self):
        # bad argument: iri
        self.assert_raises_bad_argument(
            TypeError, 2, 'iri', 'expected IRI or URIRef or str, got int',
            SPARQL_MapperStore, 'sparql-mapper', 0, SPARQL_Mapping())
        # bad argument: mapping
        self.assert_raises_bad_argument(
            TypeError, 3, 'mapping', 'expected SPARQL_Mapping, got int',
            SPARQL_MapperStore, 'sparql-mapper', 'http://x.org/', 0)
        # success
        mapping = SPARQL_Mapping()
        kb = Store('sparql-mapper', 'http://x.org/', mapping)
        self.assertIs(kb.mapping, mapping)


if __name__ == '__main__':
    TestStoreMapper_Init.main()

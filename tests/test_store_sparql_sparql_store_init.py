# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import IRI, Store
from kif_lib.store.sparql import SPARQL_Store
from kif_lib.typing import cast

from .tests import kif_StoreTestCase


class TestStoreSPARQL_SPARQL_StoreInit(kif_StoreTestCase):

    def test__init__(self):
        # bad argument: iri
        self.assert_raises_bad_argument(
            TypeError, 2, 'iri', 'cannot coerce int into IRI',
            SPARQL_Store, 'sparql', 0)
        # success
        kb = cast(SPARQL_Store, Store(
            'sparql', 'https://query.wikidata.org/sparql'))
        self.assertEqual(kb.iri, IRI('https://query.wikidata.org/sparql'))


if __name__ == '__main__':
    TestStoreSPARQL_SPARQL_StoreInit.main()

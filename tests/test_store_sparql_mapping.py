# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib.store.sparql_mapping import SPARQL_Mapping

from .tests import kif_SPARQL_MapperStoreTestCase


class TestStoreSPARQL_Mapping(kif_SPARQL_MapperStoreTestCase):

    def test_Builder(self):
        class M(SPARQL_Mapping):
            pass
        self.assertTrue(issubclass(M, SPARQL_Mapping))


if __name__ == '__main__':
    TestStoreSPARQL_Mapping.main()

# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.store.sparql_mapping import SPARQL_Mapping

from .tests import SPARQL_MapperStoreTestCase


class TestStoreSPARQL_Mapping(SPARQL_MapperStoreTestCase):

    def test_Builder(self) -> None:
        class M(SPARQL_Mapping):
            pass
        self.assertTrue(issubclass(M, SPARQL_Mapping))


if __name__ == '__main__':
    TestStoreSPARQL_Mapping.main()

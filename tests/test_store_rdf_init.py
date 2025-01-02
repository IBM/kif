# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from rdflib import Graph

from kif_lib import Store
from kif_lib.store.rdf import RDF_Store
from kif_lib.typing import cast

from .data import BENZENE_TTL, BRAZIL_TTL
from .tests import StoreTestCase


class TestStoreRDF_Init(StoreTestCase):

    def test__init__(self) -> None:
        # bad argument: graph
        self.assert_raises_bad_argument(
            TypeError, None, 'graph', 'expected Graph, got int',
            RDF_Store, 'rdf', graph=0)
        # bad argument: no such file
        self.assertRaises(
            Store.Error, Store, 'rdf', '__no_such_file__')
        # bad argument: directory
        self.assertRaises(Store.Error, Store, 'rdf', '.')
        # bad argument: unknown format
        self.assertRaises(Store.Error, Store, 'rdf', data='x')
        # bad argument: syntax error
        self.assertRaises(Store.Error, Store, 'rdf', data='x', format='ttl')
        # zero sources
        kb = Store('rdf')
        self.assertRaises(StopIteration, next, kb.filter())
        # one source
        kb = Store('rdf', BENZENE_TTL.path)
        self.assertIsInstance(kb, RDF_Store)
        # two sources
        kb = Store('rdf', BENZENE_TTL, BRAZIL_TTL)
        self.assertIsInstance(kb, RDF_Store)
        # data
        with open(BENZENE_TTL.path, encoding='utf-8') as fp:
            kb = Store('rdf', data=fp.read(), format='ttl')
            self.assertIsInstance(kb, RDF_Store)
        # graph
        g = Graph()
        kb = cast(RDF_Store, Store('rdf', graph=g, skolemize=False))
        self.assertIsInstance(kb, RDF_Store)
        self.assertIs(kb._graph, g)


if __name__ == '__main__':
    TestStoreRDF_Init.main()

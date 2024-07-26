# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from rdflib import Graph

from kif_lib import Store
from kif_lib.store.rdf import RDF_Store
from kif_lib.typing import cast

from .data import BENZENE_TTL, BRAZIL_TTL
from .tests import kif_StoreTestCase


class TestStoreRDF_Init(kif_StoreTestCase):

    def test__init__(self):
        # bad argument: graph
        self.assert_raises_bad_argument(
            TypeError, None, 'graph', 'expected Graph, got int',
            RDF_Store, 'rdf', graph=0)
        # bad argument: no such file
        self.assertRaises(
            FileNotFoundError, Store, 'rdf', '__no_such_file__')
        # bad argument: directory
        self.assertRaises(IsADirectoryError, Store, 'rdf', '.')
        # bad argument: unknown format
        self.assertRaises(Store.Error, Store, 'rdf', data='x')
        # bad argument: syntax error
        self.assertRaises(SyntaxError, Store, 'rdf', data='x', format='ttl')
        # bad argument: mutually exclusive
        self.assertRaises(ValueError, Store, 'rdf', 'x', data='x')
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
        kb = Store('rdf', data=open(BENZENE_TTL.path).read(), format='ttl')
        self.assertIsInstance(kb, RDF_Store)
        # graph
        g = Graph()
        kb = cast(RDF_Store, Store('rdf', graph=g, skolemize=False))
        self.assertIsInstance(kb, RDF_Store)
        self.assertIs(kb._graph, g)


if __name__ == '__main__':
    TestStoreRDF_Init.main()

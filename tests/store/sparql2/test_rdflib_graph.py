# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pathlib

from kif_lib import rdflib
from kif_lib.vocabulary import wd

from ...data import BENZENE_TTL
from ...tests import SPARQL_Store2TestCase


class Test(SPARQL_Store2TestCase):

    def test_default_rdflib_graph(self) -> None:
        kb = self.new_Store()
        self.assertIsNone(kb.default_rdflib_graph)

    def test__init_rdflib_graph(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'rdflib_graph', 'expected Graph, got int',
            (self.new_Store, 'SPARQL_Store2'), rdflib_graph=0)
        kb = self.new_Store()
        self.assertIsNone(kb.rdflib_graph)
        g = rdflib.Graph()
        kb = self.new_Store(rdflib_graph=g)
        self.assertIsInstance(kb.rdflib_graph, rdflib.Graph)
        # path
        self.assertRaises(kb.Error, self.new_Store, path=pathlib.Path('.'))
        self.assertRaises(
            kb.Error, self.new_Store, path=pathlib.Path(__file__))
        self.assertIsInstance(
            self.new_Store(path=BENZENE_TTL.path), type(kb))
        self.assertIsInstance(
            self.new_Store(path=str(BENZENE_TTL.path)), type(kb))
        # location
        self.assertRaises(kb.Error, self.new_Store, location=pathlib.Path('.'))
        self.assertRaises(
            kb.Error, self.new_Store, location=pathlib.Path(__file__))
        self.assertIsInstance(
            self.new_Store(location=BENZENE_TTL.path), type(kb))
        self.assertIsInstance(
            self.new_Store(location=str(BENZENE_TTL.path)), type(kb))
        # file
        with open(BENZENE_TTL.path) as fp:
            self.assertRaises(kb.Error, self.new_Store, file=BENZENE_TTL.path)
            self.assertIsInstance(self.new_Store(file=fp), type(kb))
        # data
        self.assertRaises(kb.Error, self.new_Store, data=BENZENE_TTL.path)
        self.assertIsInstance(
            self.new_Store(data=BENZENE_TTL.read()), type(kb))
        # graph
        self.assert_raises_bad_argument(
            TypeError, None, 'graph', 'cannot coerce int into Graph',
            (self.new_Store, 'SPARQL_Store2'), graph=0)
        self.assertIsInstance(self.new_Store(graph=[]), type(kb))
        self.assertIsInstance(self.new_Store(graph=[
            wd.mass(wd.benzene, 0)]), type(kb))

    def test_get_rdflib_graph(self) -> None:
        kb = self.new_Store()
        self.assertIsNone(kb.rdflib_graph)
        g = rdflib.Graph()
        kb = self.new_Store(rdflib_graph=g)
        self.assertIsInstance(kb.get_rdflib_graph(), rdflib.Graph)
        self.assertIsInstance(kb.rdflib_graph, rdflib.Graph)
        self.assertEqual(kb.get_rdflib_graph(), kb.rdflib_graph)


if __name__ == '__main__':
    Test.main()

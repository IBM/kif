# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import IRI, Item, Property
from kif_lib.context.registry import IRI_Registry, Registry
from kif_lib.typing import Any, assert_type

from ...tests import TestCase


class Test(TestCase):

    def assert_register(
            self,
            r: IRI_Registry,
            iri: IRI,
            **kwargs: Any
    ) -> None:
        self.assertEqual(r.register(iri, **kwargs), iri)

    def assert_unregister(
            self,
            r: IRI_Registry,
            iri: IRI,
            **kwargs: Any
    ) -> None:
        self.assertTrue(r.unregister(iri, **kwargs))

    def test__init__(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'prefixes', 'expected Mapping, got int',
            IRI_Registry, 0)
        self.assert_raises_bad_argument(
            TypeError, 1, 'prefixes', 'cannot coerce int into String',
            IRI_Registry, {0: 'abc'})
        self.assert_raises_bad_argument(
            TypeError, 1, 'prefixes', 'cannot coerce int into IRI',
            IRI_Registry, {'abc': 0})
        # no prefixes
        r = IRI_Registry()
        assert_type(r, IRI_Registry)
        self.assertIsInstance(r, IRI_Registry)
        self.assertIsInstance(r, Registry)
        self.assertIsNone(r.get_prefixes(IRI('a')))
        self.assertIsNone(r.get_prefixes(IRI('b')))
        self.assertIsNone(r.get_prefixes(IRI('c')))
        self.assertIsNone(r.get_prefixes(IRI('d')))
        self.assertIsNone(r.get_prefixes(IRI('e')))
        # some prefixes
        r = IRI_Registry({'a': 'b', 'c': 'd', 'e': 'd'})
        assert_type(r, IRI_Registry)
        self.assertIsInstance(r, IRI_Registry)
        self.assertIsNone(r.get_prefixes(IRI('a')))
        self.assertEqual(r.get_prefixes(IRI('b')), {'a'})
        self.assertIsNone(r.get_prefixes(IRI('c')))
        self.assertEqual(r.get_prefixes(IRI('d')), {'c', 'e'})

    def test_describe(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Property into IRI',
            r.describe, Property('x'))

    def test_register(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Property into IRI',
            r.register, Property('x'))

    def test_unregister(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.unregister, Item('x'))


if __name__ == '__main__':
    Test.main()

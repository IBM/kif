# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import IRI, Item, Lexeme, Property, Store
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
        self.assertIsNone(r.get_prefix(IRI('a')))
        self.assertIsNone(r.get_prefix(IRI('b')))
        self.assertIsNone(r.get_prefix(IRI('c')))
        self.assertIsNone(r.get_prefix(IRI('d')))
        self.assertIsNone(r.get_prefix(IRI('e')))
        # some prefixes
        r = IRI_Registry({'a': 'b', 'c': 'd', 'e': 'd'})
        assert_type(r, IRI_Registry)
        self.assertIsInstance(r, IRI_Registry)
        self.assertIsNone(r.get_prefix(IRI('a')))
        self.assertEqual(r.get_prefix(IRI('b')), 'a')
        self.assertIsNone(r.get_prefix(IRI('c')))
        self.assertEqual(r.get_prefix(IRI('d')), 'e')

    def test_curie(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce int into IRI',
            r.curie, 0)
        self.assertIsNone(r.curie(IRI('a/b')))
        self.assert_register(r, IRI('a/'), prefix='x')
        self.assertEqual(r.curie(IRI('a/b')), 'x:b')

    def test_uncurie(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'curie', 'cannot coerce int into String',
            r.uncurie, 0)
        self.assertIsNone(r.uncurie('x:b'))
        self.assert_register(r, IRI('a/'), prefix='x')
        self.assertEqual(r.uncurie('x:b'), IRI('a/b'))

    def test_lookup_resolver(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce int into IRI',
            r.lookup_resolver, 0)
        s1, s2 = Store('rdf'), Store('rdf')
        # iri
        self.assertIsNone(r.lookup_resolver(IRI('a/')))
        self.assert_register(r, IRI('a/'), resolver=s1)
        self.assertEqual(r.lookup_resolver(IRI('a/')), s1)
        self.assertEqual(r.lookup_resolver(IRI('a/b')), s1)
        self.assert_register(r, IRI('b#'), resolver=s2)
        self.assertEqual(r.lookup_resolver(IRI('b#')), s2)
        self.assertEqual(r.lookup_resolver(IRI('b#c')), s2)
        self.assertIsNone(r.lookup_resolver(IRI('c#d')))
        # entity
        for e in [Item, Property, Lexeme]:
            self.assertIsNone(r.lookup_resolver(e('a')))
            self.assertEqual(r.lookup_resolver(e('a/b')), s1)
            self.assertEqual(r.lookup_resolver(e('a/c')), s1)
            self.assertIsNone(r.lookup_resolver(e('b/c')))
            self.assertIsNone(r.lookup_resolver(e('b')))
            self.assertEqual(r.lookup_resolver(e('b#c')), s2)
            self.assertEqual(r.lookup_resolver(e('b#d')), s2)
            self.assertIsNone(r.lookup_resolver(e('c#e')))

    def test_lookup_schema(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce int into IRI',
            r.lookup_schema, 0)
        sc1 = {
            'p': IRI('http://sc1/p/'),
            'pq': IRI('http://sc1/pq/'),
            'pqv': IRI('http://sc1/pqv/'),
            'pr': IRI('http://sc1/pr/'),
            'prv': IRI('http://sc1/prv/'),
            'ps': IRI('http://sc1/ps/'),
            'psv': IRI('http://sc1/psv/'),
            'wdno': IRI('http://sc1/wdno/'),
            'wdt': IRI('http://sc1/wdt/'),
        }
        sc2 = {
            'p': IRI('http://sc2/p/'),
            'pq': IRI('http://sc2/pq/'),
            'pqv': IRI('http://sc2/pqv/'),
            'pr': IRI('http://sc2/pr/'),
            'prv': IRI('http://sc2/prv/'),
            'ps': IRI('http://sc2/ps/'),
            'psv': IRI('http://sc2/psv/'),
            'wdno': IRI('http://sc2/wdno/'),
            'wdt': IRI('http://sc2/wdt/'),
        }
        # iri
        self.assertIsNone(r.lookup_schema(IRI('a/')))
        self.assert_register(r, IRI('a/'), schema=sc1)
        self.assertEqual(r.lookup_schema(IRI('a/')), sc1)
        self.assertEqual(r.lookup_schema(IRI('a/b')), sc1)
        self.assert_register(r, IRI('b#'), schema=sc2)
        self.assertEqual(r.lookup_schema(IRI('b#')), sc2)
        self.assertEqual(r.lookup_schema(IRI('b#c')), sc2)
        self.assertIsNone(r.lookup_schema(IRI('c#d')))
        # property
        self.assertIsNone(r.lookup_schema(Property('a')))
        self.assertEqual(r.lookup_schema(Property('a/b')), sc1)
        self.assertEqual(r.lookup_schema(Property('a/c')), sc1)
        self.assertIsNone(r.lookup_schema(Property('b/c')))
        self.assertIsNone(r.lookup_schema(Property('b')))
        self.assertEqual(r.lookup_schema(Property('b#c')), sc2)
        self.assertEqual(r.lookup_schema(Property('b#d')), sc2)
        self.assertIsNone(r.lookup_schema(Property('c#e')))

    def test_describe(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Property into IRI',
            r.describe, Property('x'))
        self.assertIsNone(r.describe(IRI('x')))
        s = Store('rdf', data='')
        self.assert_register(r, IRI('x'), prefix='y', resolver=s, schema={
            'p': ('http://sc/p/'),
            'pq': ('http://sc/pq/'),
            'pqv': ('http://sc/pqv/'),
            'pr': ('http://sc/pr/'),
            'prv': ('http://sc/prv/'),
            'ps': ('http://sc/ps/'),
            'psv': ('http://sc/psv/'),
            'wdno': ('http://sc/wdno/'),
            'wdt': ('http://sc/wdt/'),
        })
        self.assertEqual(
            r.describe(IRI('x')), {'prefix': 'y', 'resolver': s, 'schema': {
                'p': IRI('http://sc/p/'),
                'pq': IRI('http://sc/pq/'),
                'pqv': IRI('http://sc/pqv/'),
                'pr': IRI('http://sc/pr/'),
                'prv': IRI('http://sc/prv/'),
                'ps': IRI('http://sc/ps/'),
                'psv': IRI('http://sc/psv/'),
                'wdno': IRI('http://sc/wdno/'),
                'wdt': IRI('http://sc/wdt/'),
            }})

    def test_get_prefix(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.get_prefix, Item('x'))
        self.assertIsNone(r.get_prefix(IRI('x')))
        self.assert_register(r, IRI('x'), prefix='y')
        self.assertEqual(r.get_prefix('x'), 'y')

    def test_get_resolver(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.get_resolver, Item('x'))
        self.assertIsNone(r.get_resolver(IRI('x')))
        s = Store('rdf')
        self.assert_register(r, IRI('x'), resolver=s)
        self.assertEqual(r.get_resolver(IRI('x')), s)

    def test_get_schema(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.get_schema, Item('x'))
        self.assertIsNone(r.get_schema(IRI('x')))
        sc = {
            'p': IRI('http://sc/p/'),
            'pq': IRI('http://sc/pq/'),
            'pqv': IRI('http://sc/pqv/'),
            'pr': IRI('http://sc/pr/'),
            'prv': IRI('http://sc/prv/'),
            'ps': IRI('http://sc/ps/'),
            'psv': IRI('http://sc/psv/'),
            'wdno': IRI('http://sc/wdno/'),
            'wdt': IRI('http://sc/wdt/'),
        }
        self.assert_register(r, IRI('x'), schema=sc)
        self.assertEqual(r.get_schema(IRI('x')), sc)

    def test_register(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Property into IRI',
            r.register, Property('x'))
        # prefix
        self.assert_raises_bad_argument(
            TypeError, None, 'prefix', 'cannot coerce int into String',
            r.register, IRI('x'), prefix=0)
        self.assertIsNone(r.describe(IRI('x')))
        self.assert_register(r, IRI('x'), prefix='a')
        self.assert_register(r, IRI('y'), prefix='b')
        self.assertEqual(r.get_prefix(IRI('x')), 'a')
        self.assertEqual(r.get_prefix(IRI('y')), 'b')
        self.assertIsNone(r.get_prefix(IRI('z')))
        self.assert_register(r, IRI('x'), prefix='a0')
        self.assertEqual(r.get_prefix(IRI('x')), 'a0')
        # resolver
        self.assert_raises_bad_argument(
            TypeError, None, 'resolver', 'expected Store, got int',
            r.register, IRI('x'), resolver=0)
        s1, s2 = Store('rdf'), Store('rdf')
        self.assert_register(r, IRI('x'), resolver=s1)
        self.assert_register(r, IRI('y'), resolver=s2)
        self.assertEqual(r.get_resolver(IRI('x')), s1)
        self.assertEqual(r.get_resolver(IRI('y')), s2)
        self.assertIsNone(r.get_resolver(IRI('z')))
        self.assert_register(r, IRI('x'), resolver=s2)
        self.assertEqual(r.get_resolver(IRI('x')), s2)
        # schema
        sc1 = {
            'p': 'http://sc1/p/',
            'pq': 'http://sc1/pq/',
            'pqv': 'http://sc1/pqv/',
            'pr': 'http://sc1/pr/',
            'prv': 'http://sc1/prv/',
            'ps': 'http://sc1/ps/',
            'psv': 'http://sc1/psv/',
            'wdno': 'http://sc1/wdno/',
            'wdt': 'http://sc1/wdt/',
        }
        sc2 = {
            'p': 'http://sc2/p/',
            'pq': 'http://sc2/pq/',
            'pqv': 'http://sc2/pqv/',
            'pr': 'http://sc2/pr/',
            'prv': 'http://sc2/prv/',
            'ps': 'http://sc2/ps/',
            'psv': 'http://sc2/psv/',
            'wdno': 'http://sc2/wdno/',
            'wdt': 'http://sc2/wdt/',
        }
        self.assert_register(r, IRI('x'), schema=sc1)
        self.assert_register(r, IRI('y'), schema=sc2)
        self.assertEqual(
            r.get_schema(IRI('x')), {k: IRI(v) for k, v in sc1.items()})
        self.assertEqual(
            r.get_schema(IRI('y')), {k: IRI(v) for k, v in sc2.items()})
        self.assertIsNone(r.get_schema(IRI('z')))
        self.assert_register(r, IRI('x'), schema=sc2)
        self.assertEqual(
            r.get_schema(IRI('x')), {k: IRI(v) for k, v in sc2.items()})

    def test_unregister(self) -> None:
        r = IRI_Registry()
        self.assert_raises_bad_argument(
            TypeError, None, 'iri', 'cannot coerce Item into IRI',
            r.unregister, Item('x'))
        # prefix
        self.assertFalse(r.unregister(IRI('x/'), prefix=True))
        self.assert_register(r, IRI('x/'), prefix='a')
        self.assert_register(r, IRI('y/'), prefix='b')
        self.assertEqual(r.get_prefix(IRI('x/')), 'a')
        self.assertEqual(r.get_prefix(IRI('y/')), 'b')
        self.assertEqual(r.curie(IRI('x/1')), 'a:1')
        self.assertEqual(r.curie(IRI('y/1')), 'b:1')
        self.assert_unregister(r, IRI('x/'), prefix=True)
        self.assertIsNone(r.get_prefix(IRI('x/')))
        self.assertEqual(r.get_prefix(IRI('y/')), 'b')
        self.assertIsNone(r.curie(IRI('x/1')))
        self.assertEqual(r.curie(IRI('y/1')), 'b:1')
        self.assert_unregister(r, IRI('y/'), prefix=True)
        self.assertIsNone(r.get_prefix(IRI('x/')))
        self.assertIsNone(r.get_prefix(IRI('y/')))
        self.assertIsNone(r.curie(IRI('x/1')))
        self.assertIsNone(r.curie(IRI('y/1')))
        # resolver
        self.assertFalse(r.unregister(IRI('x'), prefix=True))
        s = Store('rdf')
        self.assert_register(r, IRI('x'), resolver=s)
        self.assertEqual(r.get_resolver(IRI('x')), s)
        self.assert_unregister(r, IRI('x'), resolver=True)
        self.assertIsNone(r.get_resolver(IRI('x')))
        # schema
        sc = {
            'p': 'http://sc/p/',
            'pq': 'http://sc/pq/',
            'pqv': 'http://sc/pqv/',
            'pr': 'http://sc/pr/',
            'prv': 'http://sc/prv/',
            'ps': 'http://sc/ps/',
            'psv': 'http://sc/psv/',
            'wdno': 'http://sc/wdno/',
            'wdt': 'http://sc/wdt/',
        }
        self.assert_register(r, IRI('x'), schema=sc)
        self.assertEqual(
            r.get_schema(IRI('x')), {k: IRI(v) for k, v in sc.items()})
        self.assert_unregister(r, IRI('x'), schema=True)
        self.assertIsNone(r.get_schema(IRI('x')))
        # all
        self.assert_register(r, IRI('x'), prefix='a', resolver=s, schema=sc)
        self.assertIsNotNone(r.describe(IRI('x')))
        self.assert_unregister(r, IRI('x'), all=True)
        self.assertIsNone(r.describe(IRI('x')))


if __name__ == '__main__':
    Test.main()

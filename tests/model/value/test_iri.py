# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Context,
    ExternalId,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    Property,
    Store,
    String,
    StringVariable,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import Any, assert_type, Optional, Set

from ...tests import ShallowDataValueTestCase


class Test(ShallowDataValueTestCase):

    def assert_register(self, iri: IRI, **kwargs: Any) -> None:
        self.assertEqual(iri.register(**kwargs), iri)

    def assert_unregister(self, iri: IRI, **kwargs: Any) -> None:
        self.assertTrue(iri.unregister(**kwargs))

    def test_datatype_class(self) -> None:
        assert_type(IRI.datatype_class, type[IRI_Datatype])
        self.assertIs(IRI.datatype_class, IRI_Datatype)

    def test_datatype(self) -> None:
        assert_type(IRI.datatype, IRI_Datatype)
        self.assert_iri_datatype(IRI.datatype)

    def test_template_class(self) -> None:
        assert_type(IRI.template_class, type[IRI_Template])
        self.assertIs(IRI.template_class, IRI_Template)

    def test_variable_class(self) -> None:
        assert_type(IRI.variable_class, type[IRI_Variable])
        self.assertIs(IRI.variable_class, IRI_Variable)

    def test_check(self) -> None:
        assert_type(IRI.check(IRI('x')), IRI)
        self._test_check(
            IRI,
            success=[
                (ExternalId('x'), IRI('x')),
            ],
            failure=[
                IRI_Template(Variable('x')),
                Item('x'),
                Text('x'),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(IRI('x'), IRI)
        self._test__init__(
            IRI,
            self.assert_iri,
            success=[
                (['x'], IRI('x')),
                ([ExternalId('x')], IRI('x')),
            ],
            failure=[
                [IRI_Template(Variable('x'))],
                [Item('x')],
                [Text('x')],
                [Variable('x', Item)],
            ])

    def test_variables(self) -> None:
        assert_type(IRI('x').variables, Set[Variable])
        self._test_variables(IRI)

    def test_instantiate(self) -> None:
        assert_type(IRI('x').instantiate({}), Term)
        self._test_instantiate(IRI)

    def test_match(self) -> None:
        assert_type(IRI('x').match(Variable('x')), Optional[Theta])
        self._test_match(IRI, failure=[(IRI('x'), StringVariable('y'))])

    def test_split(self) -> None:
        assert_type(IRI('x').split(), tuple[IRI, str])
        self.assertEqual(IRI('').split(), (IRI('/'), ''))
        self.assertEqual(IRI('x').split(), (IRI('./'), 'x'))
        self.assertEqual(IRI('./').split(), (IRI('./'), ''))
        self.assertEqual(
            IRI('http://ex.org/').split(), (IRI('http://ex.org/'), ''))
        self.assertEqual(
            IRI('http://ex.org/abc').split(), (IRI('http://ex.org/'), 'abc'))
        self.assertEqual(
            IRI('https://ex.org/abc#def').split(),
            (IRI('https://ex.org/abc#'), 'def'))

    def test_validate(self) -> None:
        self.assertRaises(ValueError, IRI('x').validate)
        self.assertEqual(
            IRI('http://abc.org').validate(), IRI('http://abc.org'))

    def test_describe(self) -> None:
        with Context():
            assert_type(IRI('x').describe(), Optional[IRI.Descriptor])
            self.assertIsNone(IRI('x').describe())
            kb = Store('empty')
            self.assert_register(IRI('x'), prefix='y', resolver=kb)
            self.assertEqual(
                IRI('x').describe(), {'prefix': 'y', 'resolver': kb})
        self.assertIsNone(IRI('x').describe())

    def test_get_prefix(self) -> None:
        with Context():
            assert_type(IRI('x').get_prefix(), Optional[str])
            self.assertIsNone(IRI('x').get_prefix())
            self.assert_register(IRI('x'), prefix='y')
            self.assertEqual(IRI('x').get_prefix(), 'y')
            self.assertEqual(IRI('x').prefix, 'y')
            self.assert_unregister(IRI('x'))
            self.assertIsNone(IRI('x').prefix)
            self.assert_register(IRI('x'), prefix='z')
            self.assertEqual(IRI('x').prefix, 'z')
        self.assertIsNone(IRI('x').prefix)

    def test_get_resolver(self) -> None:
        with Context():
            kb1, kb2 = Store('empty'), Store('empty')
            assert_type(IRI('x').get_resolver(), Optional[Store])
            self.assertIsNone(IRI('x').get_resolver())
            self.assert_register(IRI('x'), resolver=kb1)
            self.assertEqual(IRI('x').get_resolver(), kb1)
            self.assertEqual(IRI('x').resolver, kb1)
            self.assert_unregister(IRI('x'))
            self.assertIsNone(IRI('x').resolver)
            self.assert_register(IRI('x'), resolver=kb2)
            self.assertEqual(IRI('x').resolver, kb2)
        self.assertIsNone(IRI('x').resolver)

    def test_get_schema(self) -> None:
        with Context():
            assert_type(IRI('x').get_schema(), Optional[Property.Schema])
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
            self.assertIsNone(IRI('x').get_schema())
            self.assert_register(IRI('x'), schema=sc1)
            self.assertEqual(IRI('x').get_schema(), sc1)
            self.assertEqual(IRI('x').schema, sc1)
            self.assert_unregister(IRI('x'))
            self.assertIsNone(IRI('x').schema)
            self.assert_register(IRI('x'), schema=sc2)
            self.assertEqual(IRI('x').schema, sc2)
        self.assertIsNone(IRI('x').schema)

    def test_register(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, None, 'prefix', 'cannot coerce int into String',
            IRI('x').register, prefix=0)
        self.assert_raises_bad_argument(
            TypeError, None, 'resolver', 'expected Store, got int',
            IRI('x').register, resolver=0)
        with Context():
            assert_type(IRI('x').register(), IRI)
            self.assertEqual(IRI('x').register(), IRI('x'))
            self.assertIsNone(IRI('x').describe())
            kb = Store('empty')
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
            self.assert_register(
                IRI('x'), prefix=String('y'), resolver=kb, schema=sc)
            self.assertEqual(
                IRI('x').describe(),
                {'prefix': 'y', 'resolver': kb, 'schema': sc})
            self.assert_register(IRI('x'), prefix='z')
            self.assertEqual(
                IRI('x').describe(),
                {'prefix': 'z', 'resolver': kb, 'schema': sc})
        self.assertIsNone(IRI('x').describe())

    def test_unregister(self) -> None:
        with Context():
            assert_type(IRI('x').unregister(), bool)
            self.assertIsNone(IRI('x').describe())
            kb = Store('empty')
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
            self.assert_register(
                IRI('x'), prefix='y', resolver=kb, schema=sc)
            self.assert_unregister(IRI('x'), prefix=True)
            self.assertEqual(
                IRI('x').describe(),
                {'resolver': kb, 'schema': sc})
            self.assertTrue(IRI('x').unregister())
            self.assertIsNone(IRI('x').describe())
            self.assert_register(IRI('x'), prefix='y', resolver=kb)
            self.assertEqual(
                IRI('x').describe(), {'prefix': 'y', 'resolver': kb})
            self.assert_unregister(IRI('x'), resolver=True)
            self.assertFalse(IRI('x').unregister(resolver=True))
            self.assertEqual(IRI('x').describe(), {'prefix': 'y'})
        self.assertIsNone(IRI('x').describe())


if __name__ == '__main__':
    Test.main()

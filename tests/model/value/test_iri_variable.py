# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemVariable,
    KIF_Object,
    ShallowDataValue,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(IRI_Variable, 0, IRI_Variable.check)
        self.assert_raises_check_error(IRI_Variable, {}, IRI_Variable.check)
        self.assert_raises_check_error(
            IRI_Variable, Variable('x', Item), IRI_Variable.check)
        # success
        assert_type(IRI_Variable.check(IRI_Variable('x')), IRI_Variable)
        assert_type(IRI_Variable.check(Variable('x', IRI)), IRI_Variable)
        self.assertEqual(
            IRI_Variable.check(IRI_Variable('x')), IRI_Variable('x'))
        self.assertEqual(
            IRI_Variable.check(Variable('x')),
            IRI_Variable('x'))
        self.assertEqual(
            IRI_Variable.check(Variable('x', Value)),
            IRI_Variable('x'))
        self.assertEqual(
            IRI_Variable.check(Variable('x', DataValue)),
            IRI_Variable('x'))
        self.assertEqual(
            IRI_Variable.check(Variable('x', ShallowDataValue)),
            IRI_Variable('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(IRI_Variable, 0)
        self.assert_raises_check_error(IRI_Variable, {})
        self.assert_raises_check_error(IRI_Variable, Variable('x', Item))
        # success
        assert_type(IRI_Variable('x'), IRI_Variable)
        self.assert_iri_variable(IRI_Variable('x'), 'x')
        self.assert_iri_variable(Variable('x', IRI), 'x')

    def test_coerce(self) -> None:
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, 'variable_class',
            "cannot coerce IRI_Variable into ItemVariable",
            (Variable('x', IRI).coerce, 'Variable.coerce'),
            ItemVariable)
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, 'variable_class',
            "cannot coerce IRI_Variable into ItemVariable",
            IRI_Variable('x').coerce, ItemVariable)
        # success
        x = IRI_Variable('x')
        self.assertIs(x.coerce(Value), x)
        self.assert_iri_variable(Variable('x').coerce(IRI), 'x')
        self.assert_iri_variable(Variable('x', Value).coerce(IRI), 'x')
        self.assert_iri_variable(Variable('x', DataValue).coerce(IRI), 'x')
        self.assert_iri_variable(
            Variable('x', ShallowDataValue).coerce(IRI), 'x')

    def test_instantiate(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            IRI_Variable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate IRI_Variable 'x' with Item",
            IRI_Variable('x').instantiate, {Variable('x', IRI): Item('y')})
        # success
        x = IRI_Variable('x')
        assert_type(x.instantiate({}), Optional[KIF_Object])
        self.assertIs(x.instantiate({}), x)
        self.assertIsNone(x.instantiate({x: None}))
        self.assertEqual(
            x.instantiate({x: IRI('y')}),
            IRI('y'))
        self.assertEqual(
            x.instantiate({x: IRI_Template(Variable('y'))}),
            IRI_Template(Variable('y')))
        self.assertEqual(
            x.instantiate({x: Variable('y', IRI)}),
            Variable('y', IRI))


if __name__ == '__main__':
    Test.main()

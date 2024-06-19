# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    ExternalId,
    ExternalIdTemplate,
    ExternalIdVariable,
    Item,
    ItemVariable,
    KIF_Object,
    ShallowDataValue,
    String,
    StringTemplate,
    StringVariable,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_check(self) -> None:
        self.assert_raises_check_error(
            StringVariable, 0, StringVariable.check)
        self.assert_raises_check_error(
            StringVariable, {}, StringVariable.check)
        self.assert_raises_check_error(
            StringVariable, Variable('x', Item), StringVariable.check)
        # success
        assert_type(
            StringVariable.check(StringVariable('x')), StringVariable)
        assert_type(
            StringVariable.check(Variable('x', String)), StringVariable)
        self.assertEqual(
            StringVariable.check(StringVariable('x')),
            StringVariable('x'))
        self.assertEqual(
            StringVariable.check(Variable('x')),
            StringVariable('x'))
        self.assertEqual(
            StringVariable.check(Variable('x', Value)),
            StringVariable('x'))
        self.assertEqual(
            StringVariable.check(Variable('x', DataValue)),
            StringVariable('x'))
        self.assertEqual(
            StringVariable.check(Variable('x', ShallowDataValue)),
            StringVariable('x'))
        self.assertEqual(
            StringVariable.check(Variable('x', ExternalId)),
            ExternalIdVariable('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(StringVariable, 0)
        self.assert_raises_check_error(StringVariable, {})
        self.assert_raises_check_error(StringVariable, Variable('x', Item))
        # success
        assert_type(StringVariable('x'), StringVariable)
        self.assert_string_variable(StringVariable('x'), 'x')
        self.assert_string_variable(ExternalIdVariable('x'), 'x')
        self.assert_string_variable(Variable('x', String), 'x')
        self.assert_string_variable(Variable('x', ExternalId), 'x')

    def test_coerce(self) -> None:
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, 'variable_class',
            "cannot coerce StringVariable into ItemVariable",
            (Variable('x', String).coerce, 'Variable.coerce'),
            ItemVariable)
        self.assert_raises_bad_argument(
            Variable.CoercionError, 1, 'variable_class',
            "cannot coerce StringVariable into ItemVariable",
            StringVariable('x').coerce, ItemVariable)
        # success
        x = StringVariable('x')
        self.assertIs(x.coerce(Value), x)
        self.assert_string_variable(Variable('x').coerce(String), 'x')
        self.assert_string_variable(Variable('x', Value).coerce(String), 'x')
        self.assert_string_variable(
            Variable('x', DataValue).coerce(String), 'x')
        self.assert_string_variable(
            Variable('x', ShallowDataValue).coerce(String), 'x')
        self.assert_string_variable(
            Variable('x', ExternalId).coerce(String), 'x')

    def test_instantiate(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            StringVariable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate StringVariable 'x' with Item",
            StringVariable('x').instantiate,
            {Variable('x', String): Item('y')})
        # success
        x = StringVariable('x')
        assert_type(x.instantiate({}), Optional[KIF_Object])
        self.assertIs(x.instantiate({}), x)
        self.assertIsNone(x.instantiate({x: None}))
        self.assertEqual(
            x.instantiate({x: String('y')}), String('y'))
        self.assertEqual(
            x.instantiate({x: ExternalId('y')}), ExternalId('y'))
        self.assertEqual(
            x.instantiate({x: StringTemplate(Variable('y'))}),
            StringTemplate(Variable('y')))
        self.assertEqual(
            x.instantiate({x: ExternalIdTemplate(Variable('y'))}),
            ExternalIdTemplate(Variable('y')))
        self.assertEqual(
            x.instantiate({x: Variable('y', String)}),
            Variable('y', String))
        self.assertEqual(
            x.instantiate({x: Variable('y', ExternalId)}),
            Variable('y', ExternalId))


if __name__ == '__main__':
    Test.main()

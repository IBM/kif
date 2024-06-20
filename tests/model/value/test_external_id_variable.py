# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    ExternalId,
    ExternalIdTemplate,
    ExternalIdVariable,
    Item,
    KIF_Object,
    ShallowDataValue,
    String,
    StringVariable,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(ExternalIdVariable.object_class, type[ExternalId])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ExternalIdVariable, 0, ExternalIdVariable.check)
        self.assert_raises_check_error(
            ExternalIdVariable, {}, ExternalIdVariable.check)
        self.assert_raises_check_error(
            ExternalIdVariable, Variable('x', Item),
            ExternalIdVariable.check)
        # success
        assert_type(
            ExternalIdVariable.check(ExternalIdVariable('x')),
            ExternalIdVariable)
        assert_type(
            ExternalIdVariable.check(Variable('x', ExternalIdVariable)),
            ExternalIdVariable)
        self.assertEqual(
            ExternalIdVariable.check(ExternalIdVariable('x')),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable.check(Variable('x')),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable.check(Variable('x', Value)),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable.check(Variable('x', DataValue)),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable.check(Variable('x', ShallowDataValue)),
            ExternalIdVariable('x'))
        self.assertEqual(
            ExternalIdVariable.check(Variable('x', String)),
            ExternalIdVariable('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(ExternalIdVariable, 0)
        self.assert_raises_check_error(ExternalIdVariable, {})
        self.assert_raises_check_error(ExternalIdVariable, Variable('x', Item))
        # success
        assert_type(ExternalIdVariable('x'), ExternalIdVariable)
        self.assert_string_variable(ExternalIdVariable('x'), 'x')
        self.assert_string_variable(StringVariable('x'), 'x')
        self.assert_string_variable(Variable('x', String), 'x')
        self.assert_string_variable(Variable('x', ExternalId), 'x')

    def test_instantiate(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            ExternalIdVariable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate ExternalIdVariable 'x' with Item",
            ExternalIdVariable('x').instantiate,
            {Variable('x', ExternalId): Item('y')})
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate ExternalIdVariable 'x' with String",
            ExternalIdVariable('x').instantiate,
            {Variable('x', ExternalId): String('y')})
        # success
        x = ExternalIdVariable('x')
        assert_type(x.instantiate({}), Optional[KIF_Object])
        self.assertIs(x.instantiate({}), x)
        self.assertIsNone(x.instantiate({x: None}))
        self.assertEqual(
            x.instantiate({x: ExternalId('y')}), ExternalId('y'))
        self.assertEqual(
            x.instantiate({x: ExternalIdTemplate(Variable('y'))}),
            ExternalIdTemplate(Variable('y')))
        self.assertEqual(
            x.instantiate({x: Variable('y', ExternalId)}),
            Variable('y', ExternalId))


if __name__ == '__main__':
    Test.main()

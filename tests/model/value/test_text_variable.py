# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    Item,
    KIF_Object,
    ShallowDataValue,
    Text,
    TextTemplate,
    TextVariable,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(TextVariable.object_class, type[Text])

    def test_check(self) -> None:
        self.assert_raises_check_error(TextVariable, 0, TextVariable.check)
        self.assert_raises_check_error(TextVariable, {}, TextVariable.check)
        self.assert_raises_check_error(
            TextVariable, Variable('x', Item), TextVariable.check)
        # success
        assert_type(TextVariable.check(TextVariable('x')), TextVariable)
        assert_type(TextVariable.check(Variable('x', Text)), TextVariable)
        self.assertEqual(
            TextVariable.check(TextVariable('x')), TextVariable('x'))
        self.assertEqual(
            TextVariable.check(Variable('x')),
            TextVariable('x'))
        self.assertEqual(
            TextVariable.check(Variable('x', Value)),
            TextVariable('x'))
        self.assertEqual(
            TextVariable.check(Variable('x', DataValue)),
            TextVariable('x'))
        self.assertEqual(
            TextVariable.check(Variable('x', ShallowDataValue)),
            TextVariable('x'))

    def test__init__(self) -> None:
        self.assert_raises_check_error(TextVariable, 0)
        self.assert_raises_check_error(TextVariable, {})
        self.assert_raises_check_error(TextVariable, Variable('x', Item))
        # success
        assert_type(TextVariable('x'), TextVariable)
        self.assert_text_variable(TextVariable('x'), 'x')
        self.assert_text_variable(Variable('x', Text), 'x')

    def test_instantiate(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            TextVariable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate TextVariable 'x' with Item",
            TextVariable('x').instantiate, {Variable('x', Text): Item('y')})
        # success
        x = TextVariable('x')
        assert_type(x.instantiate({}), Optional[KIF_Object])
        self.assertIs(x.instantiate({}), x)
        self.assertIsNone(x.instantiate({x: None}))
        self.assertEqual(
            x.instantiate({x: Text('y')}),
            Text('y'))
        self.assertEqual(
            x.instantiate({x: TextTemplate(Variable('y'))}),
            TextTemplate(Variable('y')))
        self.assertEqual(
            x.instantiate({x: TextTemplate(Variable('y'), Variable('z'))}),
            TextTemplate(Variable('y'), Variable('z')))
        self.assertEqual(
            x.instantiate({x: Variable('y', Text)}),
            Variable('y', Text))


if __name__ == '__main__':
    Test.main()

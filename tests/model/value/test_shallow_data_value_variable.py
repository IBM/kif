# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    DataValue,
    IRI,
    IRI_Template,
    Item,
    KIF_Object,
    ShallowDataValue,
    ShallowDataValueVariable,
    Value,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_TestCase


class Test(kif_TestCase):

    def test_object_class(self) -> None:
        assert_type(
            ShallowDataValueVariable.object_class, type[ShallowDataValue])

    def test_check(self) -> None:
        self.assert_raises_check_error(
            ShallowDataValueVariable, 0, ShallowDataValueVariable.check)
        self.assert_raises_check_error(
            ShallowDataValueVariable, {}, ShallowDataValueVariable.check)
        self.assert_raises_check_error(
            ShallowDataValueVariable, Variable('x', Item),
            ShallowDataValueVariable.check)
        # success
        assert_type(
            ShallowDataValueVariable.check(ShallowDataValueVariable('x')),
            ShallowDataValueVariable)
        assert_type(
            ShallowDataValueVariable.check(Variable('x', ShallowDataValue)),
            ShallowDataValueVariable)
        self.assertEqual(
            ShallowDataValueVariable.check(Variable('x')),
            ShallowDataValueVariable('x'))
        self.assertEqual(
            ShallowDataValueVariable.check(Variable('x', Value)),
            ShallowDataValueVariable('x'))
        self.assertEqual(
            ShallowDataValueVariable.check(Variable('x', DataValue)),
            ShallowDataValueVariable('x'))

    def test_instantiate(self) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            ShallowDataValueVariable('x').instantiate, 0)
        self.assert_raises_bad_argument(
            Variable.InstantiationError, None, None,
            "cannot instantiate ShallowDataValueVariable 'x' with Item",
            ShallowDataValueVariable('x').instantiate,
            {Variable('x', ShallowDataValueVariable): Item('y')})
        # success
        x = ShallowDataValueVariable('x')
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

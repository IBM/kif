# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Item, KIF_Object, String, Time, TimeVariable, Variable
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(TimeVariable.object_class, type[Time])
        self.assertIs(TimeVariable.object_class, Time)

    def test_check(self) -> None:
        assert_type(TimeVariable.check(TimeVariable('x')), TimeVariable)
        assert_type(TimeVariable.check(Variable('x', Time)), TimeVariable)
        self._test_check(TimeVariable)

    def test__init__(self) -> None:
        assert_type(TimeVariable('x'), TimeVariable)
        self._test__init__(TimeVariable, self.assert_time_variable)

    def test_instantiate(self) -> None:
        assert_type(
            TimeVariable('2024-06-26').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            TimeVariable,
            success=[
                Time('2024-06-26'),
                Time('2024-06-26', None, None, Variable('x')),
                Time(Variable('x'), None, Variable('y')),
                Time(Variable('y'), Variable('x')),
            ],
            failure=[
                Item('x'),
                Item.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

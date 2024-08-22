# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Property,
    Quantity,
    SomeValueSnak,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(SomeValueSnakVariable.object_class, type[SomeValueSnak])
        self.assertIs(SomeValueSnakVariable.object_class, SomeValueSnak)

    def test_check(self) -> None:
        assert_type(
            SomeValueSnakVariable.check(SomeValueSnakVariable('x')),
            SomeValueSnakVariable)
        assert_type(
            SomeValueSnakVariable.check(Variable('x', SomeValueSnak)),
            SomeValueSnakVariable)
        self._test_check(SomeValueSnakVariable)

    def test__init__(self) -> None:
        assert_type(SomeValueSnakVariable('x'), SomeValueSnakVariable)
        self._test__init__(
            SomeValueSnakVariable, self.assert_some_value_snak_variable)

    def test_instantiate(self) -> None:
        assert_type(SomeValueSnakVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            SomeValueSnakVariable,
            success=[
                SomeValueSnak('x'),
                SomeValueSnakTemplate(Variable('x')),
            ],
            failure=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Property('x'),
                Property.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

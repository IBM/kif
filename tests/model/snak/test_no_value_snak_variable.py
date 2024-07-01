# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    KIF_Object,
    NoValueSnak,
    NoValueSnakTemplate,
    NoValueSnakVariable,
    Property,
    Quantity,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(NoValueSnakVariable.object_class, type[NoValueSnak])
        self.assertIs(NoValueSnakVariable.object_class, NoValueSnak)

    def test_check(self) -> None:
        assert_type(
            NoValueSnakVariable.check(NoValueSnakVariable('x')),
            NoValueSnakVariable)
        assert_type(
            NoValueSnakVariable.check(Variable('x', NoValueSnak)),
            NoValueSnakVariable)
        self._test_check(NoValueSnakVariable)

    def test__init__(self) -> None:
        assert_type(NoValueSnakVariable('x'), NoValueSnakVariable)
        self._test__init__(
            NoValueSnakVariable, self.assert_no_value_snak_variable)

    def test_instantiate(self) -> None:
        assert_type(
            NoValueSnakVariable('x').instantiate({}),
            Optional[KIF_Object])
        self._test_instantiate(
            NoValueSnakVariable,
            success=[
                NoValueSnak('x'),
                NoValueSnakTemplate(Variable('x')),
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

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    Item,
    Property,
    Quantity,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    Term,
    ValueSnak,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(StatementVariable.object_class, type[Statement])
        self.assertIs(StatementVariable.object_class, Statement)

    def test_check(self) -> None:
        assert_type(
            StatementVariable.check(StatementVariable('x')),
            StatementVariable)
        assert_type(
            StatementVariable.check(Variable('x', Statement)),
            StatementVariable)
        self._test_check(StatementVariable)

    def test__init__(self) -> None:
        assert_type(StatementVariable('x'), StatementVariable)
        self._test__init__(StatementVariable, self.assert_statement_variable)

    def test_instantiate(self) -> None:
        assert_type(StatementVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            StatementVariable,
            success=[
                Statement(Item('x'), ValueSnak('y', 'z')),
                StatementTemplate(Variable('x'), Variable('y')),
            ],
            failure=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Property('x'),
                Property.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                SomeValueSnak(Variable('x')),
                ValueSnak('x', 'y'),
            ])


if __name__ == '__main__':
    Test.main()

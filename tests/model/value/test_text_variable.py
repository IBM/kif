# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DataValueVariable,
    EntityVariable,
    Item,
    NoValueSnak,
    Quantity,
    SnakVariable,
    String,
    StringVariable,
    Term,
    Text,
    TextTemplate,
    TextVariable,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(TextVariable.object_class, type[Text])
        self.assertIs(TextVariable.object_class, Text)

    def test_check(self) -> None:
        assert_type(TextVariable.check(TextVariable('x')), TextVariable)
        assert_type(TextVariable.check(Variable('x', Text)), TextVariable)
        self._test_check(TextVariable)

    def test__init__(self) -> None:
        assert_type(TextVariable('x'), TextVariable)
        self._test__init__(TextVariable, self.assert_text_variable)

    def test_variables(self) -> None:
        assert_type(TextVariable('x').variables, Set[Variable])
        self._test_variables(TextVariable)

    def test_instantiate(self) -> None:
        assert_type(TextVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            TextVariable,
            success_auto=[
                Text('x'),
                TextTemplate(Variable('y')),
            ],
            failure_auto=[
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
            ])

    def test_match(self) -> None:
        assert_type(TextVariable('x').match(Variable('x')), Optional[Theta])
        self._test_match(
            TextVariable,
            success=[
                (TextVariable('x'), Text('x', 'y'),
                 {TextVariable('x'): Text('x', 'y')}),
                (TextVariable('x'), Text(Variable('x')),
                 {TextVariable('x'): Text(StringVariable('x'), 'en')}),
                (TextVariable('x'), Text('x', Variable('y')),
                 {TextVariable('x'): Text('x', StringVariable('y'))}),
                (TextVariable('x'), TextVariable('y'),
                 {TextVariable('x'): TextVariable('y')}),
                (TextVariable('x'),
                 DataValueVariable('y'),
                 {DataValueVariable('y'): TextVariable('x')})
            ],
            failure=[
                (TextVariable('x'), EntityVariable('y')),
                (TextVariable('x'), Item('y')),
                (TextVariable('x'), NoValueSnak(Variable('y'))),
                (TextVariable('x'), SnakVariable('y')),
            ])


if __name__ == '__main__':
    Test.main()

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    Quantity,
    String,
    Term,
    Text,
    TextTemplate,
    TextVariable,
    Variable,
)
from kif_lib.typing import assert_type, Optional

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

    def test_instantiate(self) -> None:
        assert_type(TextVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            TextVariable,
            success=[
                Text('x'),
                TextTemplate(Variable('y')),
            ],
            failure=[
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
                String('x'),
                String.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

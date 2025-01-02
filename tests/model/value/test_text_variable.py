# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    String,
    Term,
    Text,
    TextVariable,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueVariableTestCase


class Test(ShallowDataValueVariableTestCase):

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

    def test_instantiate_and_match(self) -> None:
        assert_type(TextVariable('x').instantiate({}), Optional[Term])
        assert_type(TextVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            TextVariable,
            success=[
                Text('x'),
                Text('x', 'y'),
                Text('x', Variable('y')),
                Text(Variable('x')),
                Text(Variable('x'), Variable('y')),
            ],
            failure=[
                IRI('x'),
                IRI(Variable('x')),
                String('x'),
                String(Variable('x')),
                ExternalId('x'),
                ExternalId(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

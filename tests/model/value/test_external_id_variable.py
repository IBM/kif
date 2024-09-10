# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    ExternalIdVariable,
    IRI,
    String,
    StringVariable,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueVariableTestCase


class Test(ShallowDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(ExternalIdVariable.object_class, type[ExternalId])
        self.assertIs(ExternalIdVariable.object_class, ExternalId)

    def test_check(self) -> None:
        assert_type(
            ExternalIdVariable.check(ExternalIdVariable('x')),
            ExternalIdVariable)
        assert_type(
            ExternalIdVariable.check(Variable('x', ExternalIdVariable)),
            ExternalIdVariable)
        self._test_check(ExternalIdVariable)

    def test__init__(self) -> None:
        assert_type(ExternalIdVariable('x'), ExternalIdVariable)
        self._test__init__(
            ExternalIdVariable, self.assert_external_id_variable)

    def test_variables(self) -> None:
        assert_type(ExternalIdVariable('x').variables, Set[Variable])
        self._test_variables(ExternalIdVariable)

    def test_instantiate_and_match(self) -> None:
        assert_type(StringVariable('x').instantiate({}), Optional[Term])
        assert_type(StringVariable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            ExternalIdVariable,
            success=[
                ExternalId('x'),
                ExternalId(Variable('x')),
            ],
            failure=[
                IRI('x'),
                IRI(Variable('x')),
                String('x'),
                String(Variable('x')),
                Text('x'),
                Text(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Variable,
    String,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueVariableTestCase


class Test(ShallowDataValueVariableTestCase):

    def test_object_class(self) -> None:
        assert_type(IRI_Variable.object_class, type[IRI])
        self.assertIs(IRI_Variable.object_class, IRI)

    def test_check(self) -> None:
        assert_type(IRI_Variable.check(IRI_Variable('x')), IRI_Variable)
        assert_type(IRI_Variable.check(Variable('x', IRI)), IRI_Variable)
        self._test_check(IRI_Variable)

    def test__init__(self) -> None:
        assert_type(IRI_Variable('x'), IRI_Variable)
        self._test__init__(IRI_Variable, self.assert_iri_variable)

    def test_variables(self) -> None:
        assert_type(IRI_Variable('x').variables, Set[Variable])
        self._test_variables(IRI_Variable)

    def test_instantiate_and_match(self) -> None:
        assert_type(IRI_Variable('x').instantiate({}), Optional[Term])
        assert_type(IRI_Variable('x').match(Variable('x')), Optional[Theta])
        self._test_instantiate_and_match(
            IRI_Variable,
            success=[
                IRI('x'),
                IRI(Variable('x')),
            ],
            failure=[
                Text('x'),
                Text(Variable('x')),
                String('x'),
                String(Variable('x')),
                ExternalId('x'),
                ExternalId(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

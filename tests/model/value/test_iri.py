# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    StringVariable,
    Term,
    Text,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueTestCase


class Test(ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(IRI.datatype_class, type[IRI_Datatype])
        self.assertIs(IRI.datatype_class, IRI_Datatype)

    def test_datatype(self) -> None:
        assert_type(IRI.datatype, IRI_Datatype)
        self.assert_iri_datatype(IRI.datatype)

    def test_template_class(self) -> None:
        assert_type(IRI.template_class, type[IRI_Template])
        self.assertIs(IRI.template_class, IRI_Template)

    def test_variable_class(self) -> None:
        assert_type(IRI.variable_class, type[IRI_Variable])
        self.assertIs(IRI.variable_class, IRI_Variable)

    def test_check(self) -> None:
        assert_type(IRI.check(IRI('x')), IRI)
        self._test_check(
            IRI,
            success=[
                (ExternalId('x'), IRI('x')),
            ],
            failure=[
                IRI_Template(Variable('x')),
                Item('x'),
                Text('x'),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(IRI('x'), IRI)
        self._test__init__(
            IRI,
            self.assert_iri,
            success=[
                (['x'], IRI('x')),
                ([ExternalId('x')], IRI('x')),
            ],
            failure=[
                [IRI_Template(Variable('x'))],
                [Item('x')],
                [Text('x')],
                [Variable('x', Item)],
            ])

    def test_variables(self) -> None:
        assert_type(IRI('x').variables, Set[Variable])
        self._test_variables(IRI)

    def test_instantiate(self) -> None:
        assert_type(IRI('x').instantiate({}), Term)
        self._test_instantiate(IRI)

    def test_match(self) -> None:
        assert_type(IRI('x').match(Variable('x')), Optional[Theta])
        self._test_match(IRI, failure=[(IRI('x'), StringVariable('y'))])


if __name__ == '__main__':
    Test.main()

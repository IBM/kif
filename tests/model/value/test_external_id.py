# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    Item,
    StringVariable,
    Term,
    TextTemplate,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueTestCase


class Test(ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(ExternalId.datatype_class, type[ExternalIdDatatype])
        self.assertIs(ExternalId.datatype_class, ExternalIdDatatype)

    def test_datatype(self) -> None:
        assert_type(ExternalId.datatype, ExternalIdDatatype)
        self.assert_external_id_datatype(ExternalId.datatype)

    def test_template_class(self) -> None:
        assert_type(ExternalId.template_class, type[ExternalIdTemplate])
        self.assertIs(ExternalId.template_class, ExternalIdTemplate)

    def test_variable_class(self) -> None:
        assert_type(ExternalId.variable_class, type[ExternalIdVariable])
        self.assertIs(ExternalId.variable_class, ExternalIdVariable)

    def test_check(self) -> None:
        assert_type(ExternalId.check(ExternalId('x')), ExternalId)
        self._test_check(
            ExternalId,
            success=[
                (ExternalId('x'), ExternalId('x')),
            ],
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(ExternalId('x'), ExternalId)
        self._test__init__(
            ExternalId,
            self.assert_external_id,
            success=[
                (['x'], ExternalId('x')),
                ([ExternalId('x')], ExternalId('x')),
            ],
            failure=[
                [IRI('x')],
                [Item('x')],
                [TextTemplate(Variable('x'))],
                [Variable('x', Item)],
            ])

    def test_variables(self) -> None:
        assert_type(ExternalId('x').variables, Set[Variable])
        self._test_variables(ExternalId)

    def test_instantiate(self) -> None:
        assert_type(ExternalId('x').instantiate({}), Term)
        self._test_instantiate(ExternalId)

    def test_match(self) -> None:
        assert_type(ExternalId('x').match(Variable('x')), Optional[Theta])
        self._test_match(ExternalId, success=[
            (ExternalId('x'), StringVariable('x'),
             {StringVariable('x'): ExternalId('x')})])


if __name__ == '__main__':
    Test.main()

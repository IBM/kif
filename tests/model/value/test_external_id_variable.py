# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    ExternalIdVariable,
    Item,
    Quantity,
    String,
    StringVariable,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(StringVariable('x').instantiate({}), Optional[Term])
        assert_type(
            ExternalIdVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            ExternalIdVariable,
            success=[
                ExternalId('x'),
                ExternalIdTemplate(Variable('y')),
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

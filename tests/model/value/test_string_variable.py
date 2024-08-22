# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    IRI,
    Item,
    Quantity,
    String,
    StringTemplate,
    StringVariable,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(StringVariable.object_class, type[String])
        self.assertIs(StringVariable.object_class, String)

    def test_check(self) -> None:
        assert_type(
            StringVariable.check(StringVariable('x')), StringVariable)
        assert_type(
            StringVariable.check(Variable('x', String)), StringVariable)
        self._test_check(StringVariable)

    def test__init__(self) -> None:
        assert_type(StringVariable('x'), StringVariable)
        self._test__init__(StringVariable, self.assert_string_variable)
        self.assert_string_variable(Variable('x', ExternalId), 'x')

    def test_instantiate(self) -> None:
        assert_type(StringVariable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            StringVariable,
            success=[
                ExternalId('x'),
                ExternalIdTemplate(Variable('y')),
                String('x'),
                StringTemplate(Variable('y')),
            ],
            failure=[
                IRI('x'),
                IRI.template_class(Variable('x')),
                Item('x'),
                Item.template_class(Variable('x')),
                Quantity(0),
                Quantity.template_class(Variable('x')),
            ])


if __name__ == '__main__':
    Test.main()

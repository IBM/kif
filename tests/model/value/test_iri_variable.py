# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    Quantity,
    String,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import VariableTestCase


class Test(VariableTestCase):

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

    def test_instantiate(self) -> None:
        assert_type(IRI_Variable('x').instantiate({}), Optional[Term])
        self._test_instantiate(
            IRI_Variable,
            success=[
                IRI('x'),
                IRI_Template(Variable('y')),
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

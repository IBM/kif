# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    DatatypeVariable,
    IRI,
    IRI_Datatype,
    IRI_Variable,
    Item,
    ItemDatatype,
    ItemVariable,
    KIF_Object,
    Variable,
)
from kif_lib.typing import assert_type, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(DatatypeVariable.object_class, type[Datatype])

    def test_check(self) -> None:
        assert_type(
            DatatypeVariable.check(DatatypeVariable('x')), DatatypeVariable)
        assert_type(
            DatatypeVariable.check(Variable('x', Datatype)), DatatypeVariable)
        self._test_check(DatatypeVariable)

    def test__init__(self) -> None:
        assert_type(DatatypeVariable('x'), DatatypeVariable)
        self._test__init__(DatatypeVariable, self.assert_datatype_variable)

    def test_instantiate(self) -> None:
        assert_type(
            DatatypeVariable('x').instantiate({}), Optional[KIF_Object])
        self._test_instantiate(
            DatatypeVariable,
            success=[
                IRI_Datatype(),
                ItemDatatype(),
                DatatypeVariable('y'),
            ],
            failure=[
                IRI('x'),
                IRI_Variable('x'),
                Item('x'),
                ItemVariable('x'),
            ])


if __name__ == '__main__':
    Test.main()

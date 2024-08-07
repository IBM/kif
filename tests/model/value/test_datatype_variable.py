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
    String,
    Variable,
)
from kif_lib.typing import assert_type, cast, Optional

from ...tests import kif_VariableTestCase


class Test(kif_VariableTestCase):

    def test_object_class(self) -> None:
        assert_type(DatatypeVariable.object_class, type[Datatype])
        self.assertIs(DatatypeVariable.object_class, Datatype)

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
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): String('y')
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): IRI('y')
            })))
        self.assert_string_datatype(cast(
            Datatype, DatatypeVariable('x').instantiate({
                DatatypeVariable('x'): 'y'  # type: ignore
            })))
        self._test_instantiate(
            DatatypeVariable,
            success=[
                DatatypeVariable('y'),
                IRI_Datatype(),
                ItemDatatype(),
            ],
            failure=[
                IRI_Variable('x'),
                Item('x'),
                ItemVariable('x'),
            ])


if __name__ == '__main__':
    Test.main()

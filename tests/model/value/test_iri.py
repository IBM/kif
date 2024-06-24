# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    IRI,
    IRI_Datatype,
    IRI_Template,
    IRI_Variable,
    Item,
    Text,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTestCase


class Test(kif_ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(IRI.datatype_class, type[IRI_Datatype])

    def test_datatype(self) -> None:
        assert_type(IRI.datatype, IRI_Datatype)
        self.assertIsInstance(IRI.datatype, IRI_Datatype)

    def test_template_class(self) -> None:
        assert_type(IRI.template_class, type[IRI_Template])

    def test_variable_class(self) -> None:
        assert_type(IRI.variable_class, type[IRI_Variable])

    def test_check(self) -> None:
        assert_type(IRI.check(IRI('x')), IRI)
        self._test_check(
            IRI,
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
            ],
            failure=[
                [IRI_Template(Variable('x'))],
                [Item('x')],
                [Text('x')],
                [Variable('x', Item)],
            ])


if __name__ == '__main__':
    Test.main()

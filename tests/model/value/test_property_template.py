# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    Datatype,
    IRI,
    Item,
    KIF_Object,
    Lexeme,
    Property,
    PropertyTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_EntityTemplateTestCase


class Test(kif_EntityTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(PropertyTemplate.object_class, type[Property])

    def test_check(self) -> None:
        assert_type(
            PropertyTemplate.check(PropertyTemplate(Variable('x'))),
            PropertyTemplate)
        self._test_check(PropertyTemplate)

    def test__init__(self) -> None:
        assert_type(PropertyTemplate(Variable('x')), PropertyTemplate)
        self._test__init__(
            PropertyTemplate,
            lambda x, *y: self.assert_property_template(x, *y),
            success=[
                [IRI('x'), Variable('y', Datatype)],
                [Variable('x', IRI), None],
                [Variable('x', IRI), Variable('y', Datatype)],
            ],
            failure=[
                [Item('x')],
                [Lexeme('x')],
                [Variable('x', IRI), Variable('x', Datatype)],
            ])
        self.assert_property_template(
            PropertyTemplate(Variable('x'), Variable('y')),
            Variable('x', IRI), Variable('y', Datatype))

    def test_instantiate(self) -> None:
        assert_type(PropertyTemplate(
            Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            PropertyTemplate,
            success=[
                (PropertyTemplate(Variable('x'), Variable('y')),
                 Property('x', Item),
                 {Variable('x', IRI): IRI('x'),
                  Variable('y', Datatype): Item.datatype}),
                (PropertyTemplate('x', Variable('y')),
                 Property('x'),
                 {Variable('y', Datatype): None}),
            ],
            failure=[
                (PropertyTemplate(Variable('x'), Variable('y')),
                 {Variable('y', Datatype): Item('x')}),
            ])


if __name__ == '__main__':
    Test.main()

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    ItemTemplate,
    NoValueSnak,
    Property,
    Quantity,
    String,
    Text,
    TextSet,
    ValueSet,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ObjectSetTestCase


class Test(kif_ObjectSetTestCase):

    def test_children_class(self) -> None:
        assert_type(TextSet.children_class, type[Text])
        self.assertIs(TextSet.children_class, Text)

    def test_check(self) -> None:
        assert_type(TextSet.check('x'), TextSet)
        super()._test_check(
            TextSet,
            success=[
                ([], TextSet()),
                (('x', Text('y', 'z')),
                 TextSet(Text('x'), Text('y', 'z'))),
                (['x', String('y'), ExternalId('z')],
                 TextSet(Text('x'), Text('y'), Text('z'))),
                ({'x', 'y'},
                 TextSet(Text('x'), Text('y'))),
                (TextSet('x', 'y', 'z'),
                 TextSet(Text('x'), Text('y'), Text('z'))),
                ('xyz',
                 TextSet('x', 'y', 'z')),
                ({'x': 0, 'y': 1, 'z': 2},
                 TextSet('x', 'y', 'z')),
            ],
            failure=[
                0,
                [0],
                [Quantity(0)],
                IRI('x'),
                Item(Variable('x')),
                Property('x'),
                ValueSet(0, 1, 2),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(TextSet('x'), TextSet)
        self._test__init__(
            TextSet,
            self.assert_value_set,
            success=[
                (['x', Text('y', 'z')], TextSet(Text('x'), Text('y', 'z'))),
            ],
            failure=[
                [Item('x'), NoValueSnak('x')],
                [ItemTemplate(Variable('x'))],
                [Variable('x', Text)],
            ])

    def test_union(self) -> None:
        assert_type(TextSet().union(), TextSet)
        self.assert_value_set(TextSet().union(TextSet(), TextSet()))
        self.assert_value_set(
            TextSet('x').union(TextSet('x', 'y'), TextSet('z')),
            Text('x'), Text('y'), Text('z'))


if __name__ == '__main__':
    Test.main()

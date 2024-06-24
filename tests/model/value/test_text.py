# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    String,
    Text,
    TextDatatype,
    TextTemplate,
    TextVariable,
    Variable,
)
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTestCase


class Test(kif_ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(Text.datatype_class, type[TextDatatype])

    def test_datatype(self) -> None:
        assert_type(Text.datatype, TextDatatype)
        self.assertIsInstance(Text.datatype, TextDatatype)

    def test_template_class(self) -> None:
        assert_type(Text.template_class, type[TextTemplate])

    def test_variable_class(self) -> None:
        assert_type(Text.variable_class, type[TextVariable])

    def test_check(self) -> None:
        assert_type(Text.check(Text('x')), Text)
        self._test_check(
            Text,
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(Text('x'), Text)
        self._test__init__(
            Text,
            self.assert_text,
            success=[
                (['x', 'y'], Text('x', 'y')),
                (['x'], Text('x')),
                ([Literal('x'), 'y'], Text('x', 'y')),
                ([Literal('x'), 'y'], Text('x', 'y')),
                ([String('x'), ExternalId('y')], Text('x', 'y')),
                ([Text(ExternalId('x')), URIRef('y')], Text('x', 'y')),
                ([Text(Text('x')), String('y')], Text('x', 'y')),
                ([URIRef('x'), Literal('y')], Text('x', 'y'))
            ],
            failure=[
                ['x', 0],
                ['x', Text('y')],
                ['x', Variable('y', Item)],
                ['x', {}],
                [IRI('x')],
                [Item('x')],
                [TextTemplate(Variable('x'))],
                [Variable('x', Item)],
            ])


if __name__ == '__main__':
    Test.main()

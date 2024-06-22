# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    String,
    StringTemplate,
    StringVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_TemplateTestCase


class Test(kif_TemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ExternalIdTemplate.object_class, type[ExternalId])

    def test_check(self) -> None:
        assert_type(
            ExternalIdTemplate.check(ExternalIdTemplate(Variable('x'))),
            ExternalIdTemplate)
        self._test_check(
            ExternalIdTemplate,
            success=[
                ExternalIdTemplate(Variable('x')),
            ],
            failure=[
                ExternalId('x'),
                ExternalIdTemplate('x'),
                Item('x'),
                ItemTemplate('x'),
                String('x'),
                StringTemplate('x'),
                Variable('x'),
            ])

    def test__init__(self) -> None:
        assert_type(ExternalIdTemplate(Variable('x')), ExternalIdTemplate)
        self._test__init__(
            ExternalIdTemplate,
            lambda x, *y: self.assert_external_id_template(x, *y),
            success=[
                [StringVariable('x')],
                [Variable('x', String)],
            ],
            normalize=[
                ['x'],
                [String('x')],
            ],
            failure=[
                [IRI(Variable('x'))],
                [IRI_Variable('x')],
                [Item(IRI(Variable('x')))],
                [ItemTemplate(Variable('x'))],
                [ItemVariable('x')],
            ])

    def test_instantiate(self) -> None:
        assert_type(
            ExternalIdTemplate(Variable('x')).instantiate({}),
            KIF_Object)
        self._test_instantiate(
            ExternalIdTemplate,
            success=[
                (ExternalIdTemplate(Variable('x')),
                 ExternalId('x'),
                 {StringVariable('x'): String('x')}),
                (ExternalIdTemplate(Variable('x')),
                 ExternalId('y'),
                 {StringVariable('x'): ExternalId('y')}),
                (ExternalIdTemplate(Variable('x')),
                 ExternalIdTemplate(Variable('y')),
                 {StringVariable('x'): StringVariable('y')}),
            ],
            failure=[
                (ExternalIdTemplate(Variable('x')),
                 {StringVariable('x'): Item('x')}),
                (ExternalIdTemplate(Variable('x')),
                 {StringVariable('x'): IRI_Variable('x')}),
            ],
            failure_coerce=[
                (ExternalIdTemplate(Variable('x')),
                 {StringVariable('x'): StringTemplate(Variable('x'))}),
            ])


if __name__ == '__main__':
    Test.main()

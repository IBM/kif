# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdDatatype,
    ExternalIdTemplate,
    ExternalIdVariable,
    IRI,
    Item,
    TextTemplate,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTestCase


class Test(kif_ShallowDataValueTestCase):

    def test_datatype_class(self) -> None:
        assert_type(ExternalId.datatype_class, type[ExternalIdDatatype])

    def test_datatype(self) -> None:
        assert_type(ExternalId.datatype, ExternalIdDatatype)
        self.assertIsInstance(ExternalId.datatype, ExternalIdDatatype)

    def test_template_class(self) -> None:
        assert_type(ExternalId.template_class, type[ExternalIdTemplate])

    def test_variable_class(self) -> None:
        assert_type(ExternalId.variable_class, type[ExternalIdVariable])

    def test_check(self) -> None:
        assert_type(ExternalId.check(ExternalId('x')), ExternalId)
        self._test_check(
            ExternalId,
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])

    def test__init__(self) -> None:
        assert_type(ExternalId('x'), ExternalId)
        self._test__init__(
            ExternalId,
            self.assert_external_id,
            failure=[
                IRI('x'),
                Item('x'),
                TextTemplate(Variable('x')),
                Variable('x', Item),
            ])


if __name__ == '__main__':
    Test.main()

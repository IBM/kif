# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    StringVariable,
    Term,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTemplateTestCase


class Test(kif_ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(ExternalIdTemplate.object_class, type[ExternalId])
        self.assertIs(ExternalIdTemplate.object_class, ExternalId)

    def test_check(self) -> None:
        assert_type(
            ExternalIdTemplate.check(ExternalIdTemplate(Variable('x'))),
            ExternalIdTemplate)
        self._test_check(ExternalIdTemplate)

    def test__init__(self) -> None:
        assert_type(ExternalIdTemplate(Variable('x')), ExternalIdTemplate)
        self._test__init__(
            ExternalIdTemplate, self.assert_external_id_template)

    def test_instantiate(self) -> None:
        assert_type(
            ExternalIdTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            ExternalIdTemplate,
            success=[
                (ExternalIdTemplate(Variable('x')),
                 ExternalId('y'),
                 {StringVariable('x'): ExternalId('y')}),
            ])


if __name__ == '__main__':
    Test.main()

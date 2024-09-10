# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    ExternalIdTemplate,
    StringVariable,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueTemplateTestCase


class Test(ShallowDataValueTemplateTestCase):

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

    def test_variables(self) -> None:
        assert_type(
            ExternalIdTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(ExternalIdTemplate)

    def test_instantiate(self) -> None:
        assert_type(ExternalIdTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(ExternalIdTemplate, success=[
            (ExternalIdTemplate(Variable('x')), ExternalId('y'),
             {StringVariable('x'): ExternalId('y')}),
            (ExternalId(Variable('x')), ExternalId(Variable('y')),
             {StringVariable('x'): StringVariable('y')}),
        ], failure=[
            (ExternalId(StringVariable('x')),
             {StringVariable('x'): ExternalId(Variable('y'))}),
        ])

    def test_match(self) -> None:
        assert_type(
            ExternalIdTemplate(Variable('x')).match(ExternalId('x')),
            Optional[Theta])
        self._test_match(
            ExternalIdTemplate,
            success=[
                (ExternalId(Variable('x')), StringVariable('y'),
                 {StringVariable('y'): ExternalId(StringVariable('x'))}),
            ])


if __name__ == '__main__':
    Test.main()

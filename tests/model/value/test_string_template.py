# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    String,
    StringTemplate,
    StringVariable,
    Term,
    Variable,
)
from kif_lib.typing import assert_type, Set

from ...tests import ShallowDataValueTemplateTestCase


class Test(ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(StringTemplate.object_class, type[String])
        self.assertIs(StringTemplate.object_class, String)

    def test_check(self) -> None:
        assert_type(
            StringTemplate.check(StringTemplate(Variable('x'))),
            StringTemplate)
        self._test_check(StringTemplate)

    def test__init__(self) -> None:
        assert_type(StringTemplate(Variable('x')), StringTemplate)
        self._test__init__(StringTemplate, self.assert_string_template)

    def test_variables(self) -> None:
        assert_type(StringTemplate(Variable('x')).variables, Set[Variable])
        self._test_variables(StringTemplate)

    def test_instantiate(self) -> None:
        assert_type(
            StringTemplate(Variable('x')).instantiate({}), Term)
        self._test_instantiate(
            StringTemplate,
            success=[
                (StringTemplate(Variable('x')),
                 String('y'),
                 {StringVariable('x'): ExternalId('y')}),
            ])


if __name__ == '__main__':
    Test.main()

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    KIF_Object,
    String,
    StringTemplate,
    StringVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTemplateTestCase


class Test(kif_ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(StringTemplate.object_class, type[String])

    def test_check(self) -> None:
        assert_type(
            StringTemplate.check(StringTemplate(Variable('x'))),
            StringTemplate)
        self._test_check(StringTemplate)

    def test__init__(self) -> None:
        assert_type(StringTemplate(Variable('x')), StringTemplate)
        self._test__init__(
            StringTemplate, lambda x, *y: self.assert_string_template(x, *y))

    def test_instantiate(self) -> None:
        assert_type(
            StringTemplate(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            StringTemplate,
            success=[
                (StringTemplate(Variable('x')),
                 String('y'),
                 {StringVariable('x'): ExternalId('y')}),
            ])


if __name__ == '__main__':
    Test.main()

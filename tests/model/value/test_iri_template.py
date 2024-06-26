# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Template,
    KIF_Object,
    StringVariable,
    Variable,
)
from kif_lib.typing import assert_type

from ...tests import kif_ShallowDataValueTemplateTestCase


class Test(kif_ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(IRI_Template.object_class, type[IRI])

    def test_check(self) -> None:
        assert_type(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template)
        self._test_check(IRI_Template)

    def test__init__(self) -> None:
        assert_type(IRI_Template(Variable('x')), IRI_Template)
        self._test__init__(IRI_Template, self.assert_iri_template)

    def test_instantiate(self) -> None:
        assert_type(
            IRI_Template(Variable('x')).instantiate({}), KIF_Object)
        self._test_instantiate(
            IRI_Template,
            success=[
                (IRI_Template(Variable('x')),
                 IRI('y'),
                 {StringVariable('x'): ExternalId('y')}),
            ])


if __name__ == '__main__':
    Test.main()

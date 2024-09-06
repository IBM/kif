# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import IRI, IRI_Template, Term, Theta, Variable
from kif_lib.typing import assert_type, Optional, Set

from ...tests import ShallowDataValueTemplateTestCase


class Test(ShallowDataValueTemplateTestCase):

    def test_object_class(self) -> None:
        assert_type(IRI_Template.object_class, type[IRI])
        self.assertIs(IRI_Template.object_class, IRI)

    def test_check(self) -> None:
        assert_type(
            IRI_Template.check(IRI_Template(Variable('x'))),
            IRI_Template)
        self._test_check(IRI_Template)

    def test__init__(self) -> None:
        assert_type(IRI_Template(Variable('x')), IRI_Template)
        self._test__init__(IRI_Template, self.assert_iri_template)

    def test_variables(self) -> None:
        assert_type(IRI_Template(Variable('x')).variables, Set[Variable])
        self._test_variables(IRI_Template)

    def test_instantiate(self) -> None:
        assert_type(
            IRI_Template(Variable('x')).instantiate({}), Term)
        self._test_instantiate(IRI_Template)

    def test_match(self) -> None:
        assert_type(
            IRI_Template(Variable('x')).match(IRI('x')), Optional[Theta])
        self._test_instantiate(IRI_Template)


if __name__ == '__main__':
    Test.main()

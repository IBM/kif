# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import DataValueVariable, Item, Lexeme, Property, Term, Variable
from kif_lib.typing import Any, Iterator, override

from .value import ValueTemplateTestCase, ValueTestCase, ValueVariableTestCase


class DataValueTemplateTestCase(ValueTemplateTestCase):
    pass


class DataValueVariableTestCase(ValueVariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, DataValueVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield Item('x')
        yield Item(Variable('x'))
        yield Lexeme('x')
        yield Lexeme(Variable('x'))
        yield Property('x')
        yield Property(Variable('x'))


class DataValueTestCase(ValueTestCase):
    pass

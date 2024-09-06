# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DataValueVariable,
    Item,
    itertools,
    Lexeme,
    Property,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import Any, Iterable, override

from .value import ValueTemplateTestCase, ValueTestCase, ValueVariableTestCase


class DataValueTemplateTestCase(ValueTemplateTestCase):
    pass


class DataValueVariableTestCase(ValueVariableTestCase):

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = (),
            failure: Iterable[tuple[Term, Theta]] = (),
            success_auto: Iterable[Term] = (),
            failure_auto: Iterable[Term] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, DataValueVariable)
        super()._test_instantiate(
            cls, success=success, failure=failure,
            success_auto=success_auto, failure_auto=itertools.chain([
                Item('x'),
                Item(Variable('x')),
                Lexeme('x'),
                Lexeme(Variable('x')),
                Property('x'),
                Property(Variable('x')),
            ], failure_auto))

    @override
    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = (),
            success_auto: Iterable[Term] = (),
            failure_auto: Iterable[Term] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, DataValueVariable)
        super()._test_match(
            cls, success=success, failure=failure,
            success_auto=success_auto, failure_auto=itertools.chain([
                Item('x'),
                Item(Variable('x')),
                Lexeme('x'),
                Lexeme(Variable('x')),
                Property('x'),
                Property(Variable('x')),
            ], failure_auto))


class DataValueTestCase(ValueTestCase):
    pass

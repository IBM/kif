# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Item,
    ItemDatatype,
    itertools,
    NoValueSnak,
    SomeValueSnak,
    Statement,
    Term,
    Theta,
    ValueSnak,
    ValueVariable,
    Variable,
)
from kif_lib.typing import Any, Iterable, Iterator, override

from ..term import ClosedTermTestCase, TemplateTestCase, VariableTestCase


class ValueTemplateTestCase(TemplateTestCase):
    pass


class ValueVariableTestCase(VariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, ValueVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield ItemDatatype()
        yield ValueSnak('x', Variable('y'))
        yield SomeValueSnak('x')
        yield NoValueSnak('x')
        yield Statement(Item('x'), NoValueSnak('y'))

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
        assert issubclass(cls, ValueVariable)
        super()._test_instantiate(
            cls, success=success, failure=failure,
            success_auto=success_auto, failure_auto=itertools.chain([
                ItemDatatype(),
                NoValueSnak('x'),
                SomeValueSnak('x'),
                Statement(Item('x'), NoValueSnak('y')),
                ValueSnak('x', Variable('y')),
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
        assert issubclass(cls, ValueVariable)
        super()._test_match(
            cls, success=success, failure=failure,
            success_auto=success_auto, failure_auto=itertools.chain([
                ItemDatatype(),
                NoValueSnak(Variable('x')),
                SomeValueSnak('x'),
                Statement(Item('x'), Variable('y')),
                ValueSnak('x', 'y'),
            ], failure_auto))


class ValueTestCase(ClosedTermTestCase):
    pass

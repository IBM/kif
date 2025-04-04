# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    Item,
    itertools,
    KIF_Object,
    String,
    Term,
    Theta,
    Variable,
)
from kif_lib.typing import (
    Any,
    Callable,
    cast,
    Iterable,
    Iterator,
    override,
    Sequence,
    Set,
)

from .term import OpenTermTestCase


class VariableTestCase(OpenTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Variable)
        can_check = list(self._variable_class_can_check_from(cls))
        cannot_check = list(self._variable_class_cannot_check_from(cls))
        super()._test_check(
            cls,
            success=itertools.chain(
                map(lambda other: (Variable('x', other), Variable('x', cls)),
                    filter(lambda x: not issubclass(x, cls), can_check)),
                map(lambda other: (Variable('x', other), Variable('x', other)),
                    filter(lambda x: issubclass(x, cls), can_check)),
                success),
            failure=itertools.chain(
                map(lambda other: Variable('x', other), cannot_check),
                failure))

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Variable)
        super()._test__init__(
            cls,
            assert_fn,
            success=itertools.chain([
                (['x'], cls('x')),
                (['x'], Variable('x', cls.object_class)),
                ([String('x')], cls('x')),
                ([ExternalId('x')], cls('x')),
            ], success),
            failure=itertools.chain([
                [0],
                [IRI('x')],
                [Item('x')],
                [Variable('x')]
            ], failure))

    @override
    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Variable)
        super()._test_variables(cls, (cls('x'), {cls('x')}), *cases)

    def _test_instantiate_and_match(
            self,
            cls: Any,
            success: Iterable[Term] = (),
            failure: Iterable[Term] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Variable)
        success = list(success)
        failure = list(itertools.chain(
            self._test_instantiate_and_match_failure_auto_it(cls), failure))
        self._test_instantiate(cls, success_auto=success, failure_auto=failure)
        self._test_match(cls, success_auto=success, failure_auto=failure)

    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        return iter(())

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
        assert issubclass(cls, Variable)
        it_success: Iterable[tuple[Term, Term | None, Theta]] =\
            itertools.chain(
                success,
                [(Variable('x', cls), cls('x'), {}),
                 (Variable('x', cls), None, {cls('x'): None}),
                 (Variable('x', cls), cls('y'),
                  {cls('x'): Variable('y', cls)}),
                 ], map(lambda obj:
                        (Variable('x', cls),
                         obj, cast(Theta, {cls('x'): obj})),
                        success_auto))
        cannot_check = list(self._variable_class_cannot_check_from(cls))
        it_failure: Iterable[tuple[Term, Theta]] =\
            itertools.chain(
                failure,
                map(lambda other:
                    (Variable('x', cls), {cls('x'): other('x')}),
                    cannot_check),
                map(lambda obj:
                    (Variable('x', cls), {cls('x'): obj}), failure_auto))
        super()._test_instantiate(cls, it_success, it_failure)

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
        assert issubclass(cls, Variable)
        failure_auto_extra = map(
            lambda c: c('x'),
            filter(lambda c: not (issubclass(c, cls) or issubclass(cls, c)),
                   self.ALL_VARIABLE_CLASSES))
        super()._test_match(
            cls,
            success=itertools.chain(
                [(cls('x'), cls('y'), {cls('x'): cls('y')}),
                 (cls('x'), Variable('y'), {Variable('y'): cls('x')})],
                map(lambda term: (cls('_x'), term, {cls('_x'): term}),
                    success_auto),
                success),
            failure=itertools.chain(
                map(lambda term: (cls('_x'), term), itertools.chain(
                    failure_auto, failure_auto_extra)),
                failure))

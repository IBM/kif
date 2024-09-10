# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    IRI,
    Item,
    ItemDatatype,
    KIF_Object,
    NoValueSnak,
    Quantity,
    Snak,
    SnakTemplate,
    SnakVariable,
    Statement,
    Term,
)
from kif_lib.typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    override,
    Sequence,
)

from .term import ClosedTermTestCase, TemplateTestCase, VariableTestCase


class SnakTemplateTestCase(TemplateTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, SnakTemplate)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple(),
            failure_value_error: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, SnakTemplate)
        super()._test__init__(cls, assert_fn, success, failure, normalize)
        for t in failure_value_error:
            self.logger.debug('failure_value_error: %s', t)
            self.assertRaisesRegex(ValueError, 'cannot apply', cls, *t)


class SnakVariableTestCase(VariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, SnakVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield ItemDatatype()
        yield Item('x')
        yield IRI('x')
        yield Quantity(0)
        yield Statement(Item('x'), NoValueSnak('y'))


class SnakTestCase(ClosedTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Snak)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            failure_value_error: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Snak)
        super()._test__init__(cls, assert_fn, success, failure)
        for t in failure_value_error:
            self.logger.debug('failure_value_error: %s', t)
            self.assertRaisesRegex(ValueError, 'cannot apply', cls, *t)

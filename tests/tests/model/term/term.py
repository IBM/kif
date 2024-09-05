# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ClosedTerm, KIF_Object, OpenTerm, Term, Theta, Variable
from kif_lib.typing import Any, Callable, Iterable, override, Sequence, Set

from ..kif_object import KIF_ObjectTestCase


class TermTestCase(KIF_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        super()._test__init__(cls, assert_fn, success, failure)

    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        for term, vars in cases:
            self.assertEqual(term.variables, vars)
            self.assertEqual(term.get_variables(), vars)

    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        for src, tgt, theta in success:
            self.logger.debug('success: %s %s %s', src, tgt, theta)
            self.assertIsInstance(src, cls)
            assert isinstance(src, cls)
            self.assert_raises_bad_argument(
                TypeError, 1, 'theta', 'expected Mapping, got int',
                src.instantiate, 0)
            self.assertEqual(src.instantiate(theta), tgt)
        for obj, theta in failure:
            self.logger.debug('failure: %s %s', obj, theta)
            self.assertIsInstance(obj, cls)
            assert isinstance(obj, cls)
            self.assertRaises(
                Term.InstantiationError, obj.instantiate, theta)


class ClosedTermTestCase(TermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ClosedTerm)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ClosedTerm)
        super()._test__init__(cls, assert_fn, success, failure)


class OpenTermTestCase(TermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, OpenTerm)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, OpenTerm)
        super()._test__init__(cls, assert_fn, success, failure)

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ClosedTerm, KIF_Object, OpenTerm, Term, Theta, Variable
from kif_lib.typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    override,
    Sequence,
    Set,
)

from ..kif_object import KIF_ObjectTestCase


class TermTestCase(KIF_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = (),
            failure: Iterable[Any] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = (),
            failure: Iterable[Sequence[Any]] = (),
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
            success: Iterable[tuple[Term, Term | None, Theta]] = (),
            failure: Iterable[tuple[Term, Theta]] = ()
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

    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Term)
        for src, tgt, theta in success:
            self.logger.debug('success: %s %s %s', src, tgt, theta)
            self.assertIsInstance(src, Term)
            self.assertIsInstance(tgt, Term)
            self.assertIsInstance(theta, Mapping)
            self.assert_raises_bad_argument(
                TypeError, 1, 'other', 'cannot coerce int into Term',
                src.match, 0)
            self.assertEqual(src.match(tgt), theta)
            self.assertEqual(
                src.instantiate(theta),
                tgt.instantiate(theta))
        for src, tgt in failure:
            self.logger.debug('failure: %s %s', src, tgt)
            self.assertIsInstance(src, cls)
            assert isinstance(tgt, Term)
            self.assertIsNone(src.match(tgt))


class ClosedTermTestCase(TermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = (),
            failure: Iterable[Any] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ClosedTerm)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = (),
            failure: Iterable[Sequence[Any]] = (),
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ClosedTerm)
        super()._test__init__(cls, assert_fn, success, failure)


class OpenTermTestCase(TermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = (),
            failure: Iterable[Any] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, OpenTerm)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = (),
            failure: Iterable[Sequence[Any]] = (),
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, OpenTerm)
        super()._test__init__(cls, assert_fn, success, failure)

# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import ClosedTerm, ClosedTermSet, KIF_Object
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .term import ClosedTermTestCase


class ClosedTermSetTestCase(ClosedTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ClosedTermSet)
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
        assert issubclass(cls, ClosedTermSet)
        super()._test__init__(cls, assert_fn, success, failure)
        collect = []
        for t, obj in success:
            assert isinstance(obj, ClosedTermSet)
            for child in t:
                collect.append(child)
                self.assertIn(
                    obj.children_class.check(child), obj)  # type: ignore
            for child in t:
                if not isinstance(child, ClosedTerm):
                    self.assertNotIn(child, obj)
        self.assertEqual(
            cls(*collect),
            cls().union(*map(lambda p: p[1], success)))  # type: ignore

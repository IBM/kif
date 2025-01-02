# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Entity, Item, itertools, KIF_Object, Rank, SnakSet, Value
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .term import ClosedTermTestCase


class RankTestCase(ClosedTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Rank)
        failure = itertools.chain(
            [0, {}, Item('x'), Entity, Value, SnakSet()],
            map(lambda y: y(), filter(
                lambda x: x is not cls, Rank._get_proper_subclasses())),
            failure)
        super()._test_check(cls, success, failure)
        for other_cls in self.ALL_RANK_CLASSES - {cls}:
            if issubclass(other_cls, cls):
                continue
            if other_cls is not Rank:
                self.logger.debug('failure: %s', other_cls())
                self.assertRaisesRegex(
                    TypeError, 'cannot coerce', cls.check, other_cls())
            self.logger.debug('failure: %s', other_cls)
            self.assertRaisesRegex(
                TypeError, 'cannot coerce', cls.check, other_cls)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Rank)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([], cls()),
                *success
            ])

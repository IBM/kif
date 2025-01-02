# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import itertools, KIF_Object, Template, Term, Theta
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .term import OpenTermTestCase


class TemplateTestCase(OpenTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Template)
        super()._test_check(cls, success, itertools.chain([0, {}], failure))

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Template)
        super()._test__init__(cls, assert_fn, success, failure)
        for t in normalize:
            self.logger.debug('normalize: %s', t)
            self.assertEqual(cls(*t), cls.object_class(*t))

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Template)
        super()._test_instantiate(cls, success, failure)
        for obj, theta in failure_coerce:
            self.logger.debug('failure_coerce: %s %s', obj, theta)
            self.assertIsInstance(obj, cls)
            assert isinstance(obj, cls)
            self.assertRaises(
                Template.InstantiationError, obj.instantiate, theta)

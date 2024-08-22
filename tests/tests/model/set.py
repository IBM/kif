# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import KIF_Object, KIF_ObjectSet
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import ObjectTestCase


class ObjectSetTestCase(ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, KIF_ObjectSet)
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
        assert issubclass(cls, KIF_ObjectSet)
        super()._test__init__(cls, assert_fn, success, failure)
        collect = []
        for t, obj in success:
            assert isinstance(obj, KIF_ObjectSet)
            for child in t:
                collect.append(child)
                self.assertIn(
                    obj.children_class.check(child), obj)  # type: ignore
            for child in t:
                if not isinstance(child, KIF_Object):
                    self.assertNotIn(child, obj)
        self.assertEqual(
            cls(*collect),
            cls().union(*map(lambda p: p[1], success)))  # type: ignore

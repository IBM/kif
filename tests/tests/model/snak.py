# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Snak, SnakTemplate
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import _Obj, kif_ObjectTestCase
from .template import kif_TemplateTestCase


class kif_SnakTemplateTestCase(kif_TemplateTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, SnakTemplate)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, SnakTemplate)
        super()._test__init__(cls, assert_fn, success, failure, normalize)


class kif_SnakTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, Snak)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Snak)
        super()._test__init__(cls, assert_fn, success, failure)

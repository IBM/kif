# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import KIF_Object, Snak, SnakTemplate
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import kif_ObjectTestCase
from .template import kif_TemplateTestCase


class kif_SnakTemplateTestCase(kif_TemplateTestCase):

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


class kif_SnakTestCase(kif_ObjectTestCase):

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

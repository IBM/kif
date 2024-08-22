# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import KIF_Object
from kif_lib.typing import Any, Callable, Iterable, Sequence

from ..tests import TestCase


class KIF_ObjectTestCase(TestCase):

    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, KIF_Object)
        for v, obj in success:
            self.logger.debug('success: %s %s', v, obj)
            self.assertEqual(cls.check(v), obj)
        for v in failure:
            self.logger.debug('failure: %s', v)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls.check, v)

    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, KIF_Object)
        for t, obj in success:
            self.logger.debug('success: %s %s', t, obj)
            assert_fn(cls(*t), *obj)
        for t in failure:
            self.logger.debug('failure: %s', t)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls, *t)

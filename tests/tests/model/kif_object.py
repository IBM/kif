# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import KIF_Object
from kif_lib.typing import Any, Callable, Iterable, Sequence, TypeAlias

from ..tests import kif_TestCase

_Obj: TypeAlias = KIF_Object


class kif_ObjectTestCase(kif_TestCase):

    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v, obj in success:
            self.logger.debug('success: %s %s', v, obj)
            self.assertEqual(cls.check(v), obj)
        for v in failure:
            self.logger.debug('failure: %s', v)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls.check, v)

    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        for t, obj in success:
            self.logger.debug('success: %s %s', t, obj)
            assert_fn(cls(*t), *obj)
        for t in failure:
            self.logger.debug('failure: %s', t)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls, *t)

# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Template, Variable
from kif_lib.model import Theta
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import _Obj, kif_ObjectTestCase


class kif_TemplateTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        self.assert_raises_check_error(cls, 0, cls.check)
        self.assert_raises_check_error(cls, {}, cls.check)
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
        assert issubclass(cls, Template)
        super()._test__init__(cls, assert_fn, success, failure)
        for t in normalize:
            self.logger.debug('normalize: %s', t)
            self.assertEqual(cls(*t), cls.object_class(*t))

    def _test_instantiate(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[_Obj, _Obj, Theta]] = tuple(),
            failure: Iterable[tuple[_Obj, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[_Obj, Theta]] = tuple()
    ) -> None:
        assert issubclass(cls, Template)
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
                Variable.InstantiationError, obj.instantiate, theta)
        for obj, theta in failure_coerce:
            self.logger.debug('failure_coerce: %s %s', obj, theta)
            self.assertIsInstance(obj, cls)
            assert isinstance(obj, cls)
            self.assertRaises(TypeError, obj.instantiate, theta)

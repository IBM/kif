# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import Fingerprint, KIF_Object
from kif_lib.model import TValue
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import KIF_ObjectTestCase


class FingerprintTestCase(KIF_ObjectTestCase):

    def assert_match(self, fp: Fingerprint, *values: TValue) -> None:
        for value in values:
            self.logger.debug('success: %s %s', fp, value)
            self.assertTrue(fp.match(value))

    def assert_not_match(self, fp: Fingerprint, *values: TValue) -> None:
        for value in values:
            self.logger.debug('failure: %s %s', fp, value)
            self.assertFalse(fp.match(value))

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Fingerprint)
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
        assert issubclass(cls, Fingerprint)
        super()._test__init__(cls, assert_fn, success, failure)

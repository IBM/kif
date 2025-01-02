# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Datatype,
    Entity,
    ExternalIdDatatype,
    Item,
    itertools,
    KIF_Object,
    StringDatatype,
    Value,
)
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from ..term import ClosedTermTestCase


class DatatypeTestCase(ClosedTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Datatype)
        success = itertools.chain([
            (cls(), cls.value_class.datatype),
            (cls.value_class, cls.value_class.datatype),
            (Datatype(cls), cls.value_class.datatype),
            (Datatype(cls.value_class), cls.value_class.datatype),
        ], success)
        failure = itertools.chain([0, {}, Item('x'), Entity, Value], failure)
        super()._test_check(cls, success, failure)
        for other_cls in self.ALL_DATATYPE_CLASSES - {cls}:
            if issubclass(other_cls, cls):
                continue
            if other_cls is not Datatype:
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
        assert issubclass(cls, Datatype)
        other_cls = self.ALL_DATATYPE_CLASSES - {cls, Datatype}
        if cls is StringDatatype:
            other_cls -= {ExternalIdDatatype}
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([cls], cls()),
                ([cls], Datatype(cls)),
                ([cls.value_class], Datatype(cls.value_class)),
                *success
            ],
            failure=itertools.chain(
                map(lambda x: [x], other_cls),
                map(lambda x: [x()], other_cls),
                [[0], [Datatype]], failure))

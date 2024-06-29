# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import (
    Datatype,
    Entity,
    ExternalIdDatatype,
    Item,
    StringDatatype,
    Value,
)
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from ..kif_object import _Obj, kif_ObjectTestCase


class kif_DatatypeTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
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
                self.assert_raises_check_error(cls, other_cls(), cls.check)
            self.logger.debug('failure: %s', other_cls)
            self.assert_raises_check_error(cls, other_cls, cls.check)

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
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

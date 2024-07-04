# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import (
    Descriptor,
    ItemDescriptor,
    ItemTemplate,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Text,
    Variable,
)
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import _Obj, kif_ObjectTestCase


class kif_DescriptorTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, Descriptor)
        super()._test_check(cls, success, failure=itertools.chain([
            ItemTemplate(Variable('x')),
            Lexeme('x'),
            Property('x'),
            Text('x'),
            Variable('x', Text),
        ], failure))

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            failure_value_error: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Descriptor)
        super()._test__init__(
            cls, assert_fn, success, failure=itertools.chain([
                [0],
                [None, 0],
                [None, None, 0],
                [{}],
                [Property('x')],
                [None, ItemTemplate(Variable('x'))],
                [None, None, Lexeme('x')],
                [Property('x')],
                [Variable('x', Text)],
                [ItemDescriptor()],
                [None, LexemeDescriptor()],
                [None, None, PropertyDescriptor()],
            ], failure))

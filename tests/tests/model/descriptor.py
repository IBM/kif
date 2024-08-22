# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import (
    Descriptor,
    ItemDescriptor,
    ItemTemplate,
    KIF_Object,
    Lexeme,
    LexemeDescriptor,
    Property,
    PropertyDescriptor,
    Text,
    Variable,
)
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .kif_object import KIF_ObjectTestCase


class DescriptorTestCase(KIF_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            failure_value_error: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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

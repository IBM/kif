# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import itertools

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    ShallowDataValue,
    ShallowDataValueTemplate,
    String,
    StringTemplate,
    StringVariable,
    Variable,
)
from kif_lib.model import Theta
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from .data_value import DataValueTemplateTestCase, DataValueTestCase


class ShallowDataValueTemplateTestCase(DataValueTemplateTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test_check(
            cls,
            success=[
                (cls(Variable('x')), cls(Variable('x'))),
                *success
            ],
            failure=[
                cls('x'),
                cls.object_class('x'),
                Item('x'),
                ItemTemplate('x'),
                String('x'),
                StringTemplate('x'),
                Variable('x'),
                *failure
            ])

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([StringVariable('x')], cls(Variable('x', String))),
                *success
            ],
            failure=[
                [IRI(Variable('x'))],
                [IRI_Variable('x')],
                [Item(IRI(Variable('x')))],
                [ItemTemplate(Variable('x'))],
                [ItemVariable('x')],
                *failure
            ],
            normalize=[
                ['x'],
                [String('x')],
                *normalize
            ])

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[KIF_Object, KIF_Object, Theta]] = tuple(),
            failure: Iterable[tuple[KIF_Object, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[KIF_Object, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test_instantiate(
            cls,
            success=[
                (cls(Variable('x')),
                 cls.object_class('x'),
                 {StringVariable('x'): String('x')}),
                (cls(Variable('x')),
                 cls(Variable('y')),
                 {StringVariable('x'): StringVariable('y')}),
                *success
            ],
            failure=[
                (cls(Variable('x')),
                 {StringVariable('x'): Item('x')}),
                (cls(Variable('x')),
                 {StringVariable('x'): IRI_Variable('x')}),
                *failure
            ],
            failure_coerce=[
                (cls(Variable('x')),
                 {StringVariable('x'): StringTemplate(Variable('x'))}),
                *failure_coerce
            ])


class ShallowDataValueTestCase(DataValueTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValue)
        failure_prelude = [0, IRI(Variable('x')), Variable('x', Item), {}]
        if cls is ShallowDataValue:
            success_prelude = []
        else:
            success_prelude = [
                ('x', cls('x')),
                (cls('x'), cls('x')),
                (ExternalId('x'),
                 ExternalId('x') if cls is String else cls('x')),
                (Literal('x'), cls('x')),
                (String('x'), cls('x')),
                (URIRef('x'), cls('x')),
            ]
            failure_prelude.append(cls.template_class(Variable('x')))
        super()._test_check(
            cls,
            success=itertools.chain(success_prelude, success),
            failure=itertools.chain(failure_prelude, failure))

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, ShallowDataValue)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                (['x'], cls('x')),
                ([cls('x')], cls('x')),
                ([ExternalId('x')], cls('x')),
                ([Literal('x')], cls('x')),
                ([String('x')], cls('x')),
                ([URIRef('x')], cls('x')),
                *success
            ],
            failure=[
                [0],
                [{}],
                *failure
            ])

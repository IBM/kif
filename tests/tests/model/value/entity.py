# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import (
    Entity,
    EntityTemplate,
    ExternalId,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    String,
    StringTemplate,
    StringVariable,
    TextTemplate,
    Variable,
)
from kif_lib.model import Theta
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import Any, Callable, Iterable, override, Sequence

from ..kif_object import _Obj
from .value import kif_ValueTemplateTestCase, kif_ValueTestCase


class kif_EntityTemplateTestCase(kif_ValueTemplateTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, EntityTemplate)
        super()._test_check(
            cls,
            success=[
                (cls(Variable('x')), cls(Variable('x'))),
                (cls(IRI(Variable('x'))), cls(IRI(Variable('x')))),
                *success
            ],
            failure=[
                cls('x'),
                cls.object_class('x'),
                ExternalId(Variable('x')),
                IRI(Variable('x')),
                String(Variable('x')),
                TextTemplate(Variable('x')),
                Variable('x'),
                *failure
            ])

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, EntityTemplate)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([IRI_Template(Variable('x'))], cls(IRI(Variable('x')))),
                ([IRI_Variable('x')], cls(Variable('x', IRI))),
                *success
            ],
            failure=[
                [cls(Variable('x'))],
                [cls.object_class(IRI(Variable('x')))],
                [cls.object_class.variable_class('x')],
                [String(Variable('x'))],
                [TextTemplate(Variable('x'))],
                *failure
            ],
            normalize=[
                [cls.object_class(IRI('x'))],
                [IRI('x')],
                [String('x')],
                *normalize
            ])

    @override
    def _test_instantiate(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[_Obj, _Obj, Theta]] = tuple(),
            failure: Iterable[tuple[_Obj, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[_Obj, Theta]] = tuple()
    ) -> None:
        assert issubclass(cls, EntityTemplate)
        super()._test_instantiate(
            cls,
            success=[
                (cls(Variable('x')),
                 cls.object_class('x'),
                 {IRI_Variable('x'): IRI('x')}),
                (cls(Variable('x')),
                 cls(Variable('y')),
                 {IRI_Variable('x'): IRI_Variable('y')}),
                *success
            ],
            failure=[
                (cls(Variable('x')),
                 {IRI_Variable('x'): cls.object_class('x')}),
                (cls(Variable('x')),
                 {IRI_Variable('x'): String('x')}),
                (cls(Variable('x')),
                 {IRI_Variable('x'): StringVariable('x')}),
                (cls(Variable('x')),
                 {IRI_Variable('x'): StringTemplate('x')}),
                *failure
            ],
            failure_coerce=failure_coerce)


class kif_EntityTestCase(kif_ValueTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, Entity)
        failure_prelude = [0, IRI(Variable('x')), Variable('x', Item), {}]
        if cls is Entity:
            success_prelude = []
        else:
            success_prelude = [
                ('x', cls('x')),
                (cls('x'), cls('x')),
                (ExternalId('x'), cls('x')),
                (IRI('x'), cls('x')),
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
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Entity)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([cls('x')], cls('x')),
                ([ExternalId('x')], cls('x')),
                ([IRI('x')], cls('x')),
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

    def _test_Entities(
            self,
            map_fn: Callable[..., Iterable[_Obj]],
            assert_fn: Callable[..., None],
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v in failure:
            self.assertRaises(TypeError, list, map_fn, v)
        a, b, c = map_fn('a', IRI('b'), 'c')
        assert_fn(a, IRI('a'))
        assert_fn(b, IRI('b'))
        assert_fn(c, IRI('c'))

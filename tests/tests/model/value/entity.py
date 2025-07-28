# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    itertools,
    KIF_Object,
    PseudoProperty,
    Quantity,
    String,
    StringTemplate,
    StringVariable,
    Term,
    Text,
    TextTemplate,
    Theta,
    Time,
    Variable,
)
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    override,
    Sequence,
    Set,
)

from .value import ValueTemplateTestCase, ValueTestCase, ValueVariableTestCase


class EntityTemplateTestCase(ValueTemplateTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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
                cls.object_class('x'),  # pyright: ignore
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
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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
    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, EntityTemplate)
        super()._test_variables(
            cls, (cls(Variable('x')), {IRI_Variable('x')}), *cases)

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, EntityTemplate)
        super()._test_instantiate(
            cls,
            success=[
                (cls(Variable('x')),
                 cls.object_class('x'),  # pyright: ignore
                 {IRI_Variable('x'): IRI('x')}),
                (cls(Variable('x')),
                 cls(Variable('y')),
                 {IRI_Variable('x'): IRI_Variable('y')}),
                *success
            ],
            failure=[
                (cls(Variable('x')),
                 {IRI_Variable('x'):
                  cls.object_class('x')}),  # pyright: ignore
                (cls(Variable('x')),
                 {IRI_Variable('x'): String('x')}),
                (cls(Variable('x')),
                 {IRI_Variable('x'): StringVariable('x')}),
                (cls(Variable('x')),
                 {IRI_Variable('x'): StringTemplate('x')}),
                *failure
            ],
            failure_coerce=failure_coerce)

    @override
    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, EntityTemplate)
        super()._test_match(
            cls,
            success=itertools.chain([
                (cls(Variable('x')), cls('x'),
                 {IRI_Variable('x'): IRI('x')}),
                (cls(Variable('x')), cls(Variable('y')),
                 {IRI_Variable('x'): IRI_Variable('y')}),
                (cls(Variable('x')), cls.object_class.variable_class('y'),
                 {cls.object_class.variable_class('y'): cls(Variable('x'))}),
            ], success),
            failure=itertools.chain([
                (cls(Variable('x')), IRI_Variable('y')),
                (cls(Variable('x')), IRI('y')),
            ], failure))


class EntityVariableTestCase(ValueVariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, EntityVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield IRI('x')
        yield IRI(Variable('x'))
        yield Text('x')
        yield Text(Variable('x'))
        yield Text('x', Variable('y'))
        yield String('x')
        yield String(Variable('x'))
        yield ExternalId('x')
        yield ExternalId(Variable('x'))
        yield Quantity(0)
        yield Quantity(Variable('x'))
        yield Time('2024-09-09')
        yield Time(Variable('x'))


class EntityTestCase(ValueTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Entity)
        failure_prelude = [0, IRI(Variable('x')), Variable('x', Item), {}]
        if cls is Entity or issubclass(cls, PseudoProperty):
            success_prelude = []
        else:
            success_prelude = [
                ('x', cls('x')),             # pyright: ignore
                (cls('x'), cls('x')),        # pyright: ignore
                (ExternalId('x'), cls('x')),  # pyright: ignore
                (IRI('x'), cls('x')),         # pyright: ignore
                (Literal('x'), cls('x')),     # pyright: ignore
                (String('x'), cls('x')),      # pyright: ignore
                (URIRef('x'), cls('x')),      # pyright: ignore
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
        assert isinstance(cls, type)
        assert issubclass(cls, Entity)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([cls('x')], cls('x')),        # pyright: ignore
                ([ExternalId('x')], cls('x')),  # pyright: ignore
                ([IRI('x')], cls('x')),         # pyright: ignore
                ([Literal('x')], cls('x')),     # pyright: ignore
                ([String('x')], cls('x')),      # pyright: ignore
                ([URIRef('x')], cls('x')),      # pyright: ignore
                *success
            ],
            failure=[
                [0],
                [{}],
                *failure
            ])

    @override
    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Entity)
        super()._test_variables(
            cls, (cls('x'), set()), *cases)  # pyright: ignore

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Entity)
        super()._test_instantiate(
            cls,
            success=itertools.chain(
                [(cls('x'), cls('x'),  # pyright: ignore
                  {IRI_Variable('x'): IRI_Variable('y')})],
                success), failure=failure)

    @override
    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Entity)
        super()._test_match(
            cls,
            success=itertools.chain([
                (cls('x'), cls('x'), {}),         # pyright: ignore
                (cls('x'), Variable('x', cls),    # pyright: ignore
                 {Variable('x', cls): cls('x')}),  # pyright: ignore
                (Variable('x', cls), cls('x'),     # pyright: ignore
                 {Variable('x', cls): cls('x')})   # pyright: ignore
            ], success),
            failure=itertools.chain([
                (cls('x'), IRI_Variable('y'))], failure))  # pyright: ignore

    def _test_Entities(
            self,
            map_fn: Callable[..., Iterable[KIF_Object]],
            assert_fn: Callable[..., None],
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v in failure:
            self.assertRaises(TypeError, list, map_fn, v)
        a, b, c = map_fn('a', IRI('b'), 'c')
        assert_fn(a, IRI('a'))
        assert_fn(b, IRI('b'))
        assert_fn(c, IRI('c'))

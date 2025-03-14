# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    itertools,
    KIF_Object,
    Quantity,
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
    String,
    StringTemplate,
    StringVariable,
    Term,
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

from .data_value import (
    DataValueTemplateTestCase,
    DataValueTestCase,
    DataValueVariableTestCase,
)


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
    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test_variables(
            cls, (cls(Variable('x')), {StringVariable('x')}), *cases)

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test_instantiate(
            cls,
            success=itertools.chain([
                (cls(Variable('x')),
                 cls.object_class('x'),
                 {StringVariable('x'): String('x')}),
                (cls(Variable('x')),
                 cls.object_class('y'),
                 {StringVariable('x'): ExternalId('y')}),
                (cls(Variable('x')),
                 cls(Variable('y')),
                 {StringVariable('x'): StringVariable('y')}),
            ], success),
            failure=itertools.chain([
                (cls(Variable('x')),
                 {StringVariable('x'): Item('x')}),
                (cls(Variable('x')),
                 {StringVariable('x'): IRI_Variable('x')}),
            ], failure),
            failure_coerce=itertools.chain([
                (cls(Variable('x')),
                 {StringVariable('x'): StringTemplate(Variable('x'))}),
            ], failure_coerce))

    @override
    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueTemplate)
        super()._test_match(
            cls,
            success=itertools.chain([
                (cls(Variable('x')), cls('x'),
                 {StringVariable('x'): String('x')}),
                (cls(Variable('x')), cls(Variable('y')),
                 {StringVariable('x'): StringVariable('y')}),
                (cls(Variable('x')), cls.object_class.variable_class('y'),
                 {cls.object_class.variable_class('y'): cls(Variable('x'))}),
            ], success),
            failure=itertools.chain(
                [(cls(Variable('x')), Item('y'))], failure))


class ShallowDataValueVariableTestCase(DataValueVariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValueVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield Quantity(0)
        yield Quantity(Variable('x'))
        yield Time('2024-09-09')
        yield Time(Variable('x'))


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

    @override
    def _test_variables(
            self,
            cls: Any,
            *cases: tuple[Term, Set[Variable]]
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValue)
        super()._test_variables(cls, (cls('x'), set()), *cases)

    @override
    def _test_instantiate(
            self,
            cls: Any,
            success: Iterable[tuple[Term, Term | None, Theta]] = tuple(),
            failure: Iterable[tuple[Term, Theta]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValue)
        super()._test_instantiate(
            cls,
            success=itertools.chain(
                [(cls('x'), cls('x'), {StringVariable('x'): String('y')})],
                success), failure=failure)

    @override
    def _test_match(
            self,
            cls,
            success: Iterable[tuple[Term, Term, Theta]] = (),
            failure: Iterable[tuple[Term, Term]] = ()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, ShallowDataValue)
        super()._test_match(
            cls,
            success=itertools.chain([
                (cls('x'), cls('x'), {}),
                (cls('x'), Variable('x', cls), {Variable('x', cls): cls('x')}),
                (Variable('x', cls), cls('x'), {Variable('x', cls): cls('x')})
            ], success))

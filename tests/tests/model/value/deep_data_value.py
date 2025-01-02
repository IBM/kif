# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DeepDataValue,
    DeepDataValueTemplate,
    DeepDataValueVariable,
    ExternalId,
    IRI,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    itertools,
    KIF_Object,
    String,
    StringTemplate,
    Term,
    Text,
    Variable,
)
from kif_lib.typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    override,
    Sequence,
)

from .data_value import (
    DataValueTemplateTestCase,
    DataValueTestCase,
    DataValueVariableTestCase,
)


class DeepDataValueTemplateTestCase(DataValueTemplateTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, DeepDataValueTemplate)
        super()._test_check(
            cls,
            success=[
                (cls(Variable('x')), cls(Variable('x'))),
                *success
            ],
            failure=[
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
        assert issubclass(cls, DeepDataValueTemplate)
        super()._test__init__(
            cls,
            assert_fn,
            success=[
                ([Variable('x')], cls(Variable('x'))),
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
            normalize=normalize)


class DeepDataValueVariableTestCase(DataValueVariableTestCase):

    @override
    def _test_instantiate_and_match_failure_auto_it(
            self,
            cls: Any
    ) -> Iterator[Term]:
        assert isinstance(cls, type)
        assert issubclass(cls, DeepDataValueVariable)
        yield from super()._test_instantiate_and_match_failure_auto_it(cls)
        yield IRI('x')
        yield IRI(Variable('x'))
        yield Text('x')
        yield Text(Variable('x'))
        yield String('x')
        yield String(Variable('x'))
        yield ExternalId('x')
        yield ExternalId(Variable('x'))


class DeepDataValueTestCase(DataValueTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple(),
            failure_value_error: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, DeepDataValue)
        failure_prelude = [
            IRI(Variable('x')),
            Item('x'),
            Variable('x'),
            {},
        ]
        if cls is not DeepDataValue:
            failure_prelude.append(cls.template_class(Variable('x')))
        super()._test_check(
            cls,
            success=success,
            failure=itertools.chain(failure_prelude, failure))
        for t in failure_value_error:
            self.logger.debug('failure_value_error: %s', t)
            self.assertRaisesRegex(
                ValueError, 'cannot coerce', cls.check, *t)

    @override
    def _test__init__(
            self,
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, DeepDataValue)
        super()._test__init__(
            cls, assert_fn, success=success,
            failure=[
                [cls.template_class(Variable('x'))],
                [Item('x')],
                [{}],
                *failure
            ])

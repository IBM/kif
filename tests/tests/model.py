# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import (
    Datatype,
    Entity,
    EntityTemplate,
    ExternalId,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    ShallowDataValueTemplate,
    String,
    StringTemplate,
    StringVariable,
    Template,
    TextTemplate,
    Value,
    Variable,
)
from kif_lib.model import DatatypeClass, Theta, VariableClass
from kif_lib.rdflib import Literal, URIRef
from kif_lib.typing import (
    Any,
    Callable,
    cast,
    Iterable,
    override,
    Sequence,
    TypeAlias,
)

from .common import kif_TestCase

_Obj: TypeAlias = KIF_Object  # TypeVar('_Obj', bound=KIF_Object)


class kif_ObjectTestCase(kif_TestCase):

    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v, obj in success:
            self._debug('success:', v, obj)
            self.assertEqual(cls.check(v), obj)
        for v in failure:
            self._debug('failure:', v)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls.check, v)

    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        for t, obj in success:
            self._debug('success:', t, obj)
            assert_fn(cls(*t), *obj)
        for t in failure:
            self._debug('failure:', t)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls, *t)


class kif_TemplateTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        self.assert_raises_check_error(cls, 0, cls.check)
        self.assert_raises_check_error(cls, {}, cls.check)
        super()._test_check(cls, success, failure)

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Template)
        super()._test__init__(cls, assert_fn, success, failure)
        for t in normalize:
            self._debug('normalize:', t)
            self.assertEqual(cls(*t), cls.object_class(*t))

    def _test_instantiate(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[_Obj, _Obj, Theta]] = tuple(),
            failure: Iterable[tuple[_Obj, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[_Obj, Theta]] = tuple()
    ) -> None:
        assert issubclass(cls, Template)
        for src, tgt, theta in success:
            self._debug('success:', src, tgt, theta)
            self.assertIsInstance(src, cls)
            assert isinstance(src, cls)
            self.assert_raises_bad_argument(
                TypeError, 1, 'theta', 'expected Mapping, got int',
                src.instantiate, 0)
            self.assertEqual(src.instantiate(theta), tgt)
        for obj, theta in failure:
            self._debug('failure (instantiation):', obj, theta)
            self.assertIsInstance(obj, cls)
            assert isinstance(obj, cls)
            self.assertRaises(
                Variable.InstantiationError, obj.instantiate, theta)
        for obj, theta in failure_coerce:
            self._debug('failure (coerce):', obj, theta)
            self.assertIsInstance(obj, cls)
            assert isinstance(obj, cls)
            self.assertRaises(TypeError, obj.instantiate, theta)


class kif_EntityTemplateTestCase(kif_TemplateTestCase):

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


class kif_ShallowDataValueTemplateTestCase(kif_TemplateTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
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
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple(),
            normalize: Iterable[Sequence[Any]] = tuple()
    ) -> None:
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
            cls: type[_Obj],
            success: Iterable[tuple[_Obj, _Obj, Theta]] = tuple(),
            failure: Iterable[tuple[_Obj, Theta]] = tuple(),
            failure_coerce: Iterable[tuple[_Obj, Theta]] = tuple()
    ) -> None:
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


class kif_VariableTestCase(kif_ObjectTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert issubclass(cls, Variable)
        can_check = list(self._variable_class_can_check_from(cls))
        cannot_check = list(self._variable_class_cannot_check_from(cls))
        super()._test_check(
            cls,
            success=itertools.chain(
                map(lambda other: (Variable('x', other), Variable('x', cls)),
                    filter(lambda x: not issubclass(x, cls), can_check)),
                map(lambda other: (Variable('x', other), Variable('x', other)),
                    filter(lambda x: issubclass(x, cls), can_check)),
                success),
            failure=itertools.chain(
                map(lambda other: Variable('x', other), cannot_check),
                failure))

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert issubclass(cls, Variable)
        super()._test__init__(
            cls,
            assert_fn,
            success=itertools.chain([
                (['x'], cls('x')),
                (['x'], Variable('x', cls.object_class)),
                ([String('x')], cls('x')),
                ([ExternalId('x')], cls('x')),
            ], success),
            failure=itertools.chain([
                [0],
                [IRI('x')],
                [Item('x')],
                [Variable('x')]
            ], failure))

    def _test_instantiate(
            self,
            cls: VariableClass,
            success: Iterable[_Obj] = tuple(),
            failure: Iterable[_Obj] = tuple()
    ) -> None:
        self.assert_raises_bad_argument(
            TypeError, 1, 'theta', 'expected Mapping, got int',
            cls('x').instantiate, 0)
        for obj in failure:
            self.assert_raises_bad_argument(
                Variable.InstantiationError, None, None,
                f"cannot instantiate {cls.__qualname__} 'x' with "
                f'{type(obj).__qualname__}',
                cls('x').instantiate,
                {Variable('x', cls.object_class): obj})
        # success
        x = cls('x')
        self.assertIs(x.instantiate({}), x)
        self.assertIsNone(x.instantiate({x: None}))
        self.assertEqual(
            x.instantiate({x: Variable('y', cls)}),
            Variable('y', cls))
        for obj in success:
            self.assertEqual(x.instantiate({x: obj}), obj)


class kif_DatatypeTestCase(kif_TestCase):

    def _test_check(self, cls: DatatypeClass) -> None:
        assert issubclass(cls, Datatype)
        self.assert_raises_check_error(cls, 0, cls.check)
        self.assert_raises_check_error(cls, {}, cls.check)
        self.assert_raises_check_error(cls, Item('x'), cls.check)
        self.assert_raises_check_error(cls, Entity, cls.check)
        self.assert_raises_check_error(cls, Value, cls.check)
        for other_cls in self.ALL_DATATYPE_CLASSES - {cls}:
            if issubclass(other_cls, cls):
                continue
            if other_cls is not Datatype:
                self.assert_raises_check_error(cls, other_cls(), cls.check)
            self.assert_raises_check_error(cls, other_cls, cls.check)
        # success
        self.assertEqual(cls.check(cls()), cls.value_class.datatype)
        self.assertEqual(cls.check(Datatype(cls)), cls.value_class.datatype)
        self.assertEqual(
            cls.check(Datatype(cls.value_class)), cls.value_class.datatype)
        self.assertEqual(
            cls.check(cls.value_class), cls.value_class.datatype)

    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None]
    ) -> None:
        assert issubclass(cls, Datatype)
        self.assert_raises_check_error(cls, 0)
        # success
        assert_fn(cls())
        assert_fn(cast(_Obj, Datatype(cls)))
        assert_fn(cast(_Obj, Datatype(cls.value_class)))


class kif_ValueTestCase(kif_ObjectTestCase):

    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v in failure:
            self._debug('failure:', v)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls.check, v)
        for v, obj in success:
            self._debug('success:', v, obj)
            self.assertEqual(cls.check(v), obj)

    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        for t in failure:
            self._debug('failure:', t)
            self.assertRaisesRegex(TypeError, 'cannot coerce', cls, *t)
        for t, obj in success:
            self._debug('success:', t, obj)
            assert_fn(cls(*t), *obj)


class kif_EntityTestCase(kif_ValueTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        self.assert_raises_check_error(IRI, 0, cls.check)
        self.assert_raises_check_error(IRI, {}, cls.check)
        self.assert_raises_check_error(
            IRI, IRI_Template(Variable('x')), cls.check)
        self.assert_raises_check_error(IRI, Variable('x'), cls.check)
        super()._test_check(
            cls,
            success=[
                ('x', cls('x')),
                (cls('x'), cls('x')),
                (ExternalId('x'), cls('x')),
                (IRI('x'), cls('x')),
                (Literal('x'), cls('x')),
                (String('x'), cls('x')),
                (URIRef('x'), cls('x')),
                *success
            ],
            failure=[
                0, {}, Variable('x', Item), *failure
            ])

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        self.assert_raises_check_error(IRI, 0, cls, None, 1)
        self.assert_raises_check_error(IRI, {}, cls, None, 1)
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
                [0], [{}], *failure
            ])

    def _test_Entities(
            self,
            map_fn: Callable[..., Iterable[_Obj]],
            assert_fn: Callable[..., None],
            failure: Iterable[Any] = tuple()
    ) -> None:
        for v in failure:
            self.assertRaises(TypeError, list, map_fn, v)
        # success
        a, b, c = map_fn('a', IRI('b'), 'c')
        assert_fn(a, IRI('a'))
        assert_fn(b, IRI('b'))
        assert_fn(c, IRI('c'))


class kif_DataValueTestCase(kif_ValueTestCase):
    pass


class kif_ShallowDataValueTestCase(kif_DataValueTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        self.assert_raises_check_error(cls, 0)
        self.assert_raises_check_error(cls, {})
        self.assert_raises_check_error(
            cls, cls.template_class(Variable('x')))
        self.assert_raises_check_error(cls, Variable('x'))
        super()._test_check(
            cls,
            success=[
                ('x', cls('x')),
                (cls('x'), cls('x')),
                (Literal('x'), cls('x')),
                (String('x'), cls('x')),
                (URIRef('x'), cls('x')),
                *success
            ],
            failure=failure)
        if cls is not String:
            self.assertEqual(cls.check(ExternalId('x')), cls('x'))
        else:
            self.assertEqual(cls.check(ExternalId('x')), ExternalId('x'))

    @override
    def _test__init__(
            self,
            cls: type[_Obj],
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], _Obj]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        self.assert_raises_check_error(String, 0, cls, None, 1)
        self.assert_raises_check_error(String, {}, cls, None, 1)
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
            failure=failure)


class kif_DeepDataValueTestCase(kif_DataValueTestCase):

    @override
    def _test_check(
            self,
            cls: type[_Obj],
            success: Iterable[tuple[Any, _Obj]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        self.assert_raises_check_error(cls, {})
        self.assert_raises_check_error(
            cls, cls.template_class(Variable('x')))
        self.assert_raises_check_error(cls, Variable('x'))
        super()._test_check(cls, success, failure)

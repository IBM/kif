# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import itertools

from kif_lib import ExternalId, IRI, Item, KIF_Object, String, Term, Variable
from kif_lib.model import Theta
from kif_lib.typing import (
    Any,
    Callable,
    cast,
    Iterable,
    Optional,
    override,
    Sequence,
)

from .term import kif_OpenTermTestCase


class kif_VariableTestCase(kif_OpenTermTestCase):

    @override
    def _test_check(
            self,
            cls: Any,
            success: Iterable[tuple[Any, KIF_Object]] = tuple(),
            failure: Iterable[Any] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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
            cls: Any,
            assert_fn: Callable[..., None],
            success: Iterable[tuple[Sequence[Any], KIF_Object]] = tuple(),
            failure: Iterable[Sequence[Any]] = tuple()
    ) -> None:
        assert isinstance(cls, type)
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
            cls: Any,
            success: Iterable[Term] = tuple(),
            failure: Iterable[Term] = tuple()
    ) -> None:
        assert isinstance(cls, type)
        assert issubclass(cls, Variable)
        it_success: Iterable[tuple[Term, Optional[Term], Theta]] =\
            itertools.chain([
                (Variable('x', cls), cls('x'), {}),
                (Variable('x', cls), None, {cls('x'): None}),
                (Variable('x', cls), cls('y'),
                 {cls('x'): Variable('y', cls)}),
            ], map(lambda obj:
                   (Variable('x', cls), obj, cast(Theta, {cls('x'): obj})),
                   success))
        for src, tgt, theta in it_success:
            self.logger.debug('success: %s %s %s', src, tgt, theta)
            self.assertIsInstance(src, cls)
            assert isinstance(src, cls)
            self.assert_raises_bad_argument(
                TypeError, 1, 'theta', 'expected Mapping, got int',
                src.instantiate, 0)
            self.assertEqual(src.instantiate(cast(Theta, theta)), tgt)
        cannot_check = list(self._variable_class_cannot_check_from(cls))
        it_failure: Iterable[tuple[KIF_Object, Theta]] =\
            itertools.chain(
            map(lambda other: (Variable('x', cls), {cls('x'): other('x')}),
                cannot_check),
            map(lambda obj: (Variable('x', cls), {cls('x'): obj}), failure))
        for obj, theta in it_failure:
            self.logger.debug('failure: %s %s', obj, theta)
            self.assertRaises(
                Variable.InstantiationError, cls('x').instantiate, theta)

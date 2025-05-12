# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from kif_lib import (
    Context,
    Filter,
    Item,
    itertools,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
)
from kif_lib.context import Section
from kif_lib.typing import Any, Callable, Sequence, TypeVar, Union

from ..tests import TestCase

T = TypeVar('T')


class Test(TestCase):

    def _test_option_bool(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, bool]] = (),
            envvars: Sequence[str] = (),
            optional: bool = False
    ) -> None:
        self._test_option(
            section=section,
            name=name,
            values=[
                (False, False),
                (True, True),
                (None, False),
                (0, False),
                (1, True),
                *values] + [(None, None)] if optional else [],
            envvars=envvars)

    def _test_option_float(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, float]] = (),
            envvars: Sequence[str] = (),
            lower_bound: float | None = None,
            upper_bound: float | None = None,
            optional: bool = False
    ) -> None:
        def norm(x: float | None) -> float | None:
            if x is None:
                return None
            assert (
                lower_bound is None
                or upper_bound is None
                or lower_bound < upper_bound)
            if lower_bound is not None and x < lower_bound:
                return lower_bound
            if upper_bound is not None and x > upper_bound:
                return upper_bound
            return x
        self._test_option(
            section=section,
            name=name,
            values=[
                (0., norm(0.)),
                (1., norm(1.)),
                (-33., norm(-33.)),
                (8., norm(8.)),
                (42., norm(42.)),
                *values] + [(None, None)] if optional else [],
            envvars=envvars,
            type_error={})

    def _test_option_int(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, int]] = (),
            envvars: Sequence[str] = (),
            lower_bound: int | None = None,
            upper_bound: int | None = None,
            optional: bool = False
    ) -> None:
        def norm(x: int | None) -> int | None:
            if x is None:
                return None
            assert (
                lower_bound is None
                or upper_bound is None
                or lower_bound < upper_bound)
            if lower_bound is not None and x < lower_bound:
                return lower_bound
            if upper_bound is not None and x > upper_bound:
                return upper_bound
            return x
        self._test_option(
            section=section,
            name=name,
            values=[
                (0, norm(0)),
                (1, norm(1)),
                (-33, norm(-33)),
                (8, norm(8)),
                (42, norm(42)),
                *values] + [(None, None)] if optional else [],
            envvars=envvars,
            type_error={})

    def _test_option(
            self,
            section: Callable[[Context], Section],
            name: str,
            values: Sequence[tuple[Any, Any]],
            envvars: Sequence[str] = (),
            type_error: Any | None = None,
            value_error: Any | None = None
    ) -> None:
        def get_fn(opts: Section) -> Any:
            return getattr(opts, name)

        def set_fn(opts: Section, value: Any) -> None:
            setattr(opts, name, value)
        default_name = 'DEFAULT_' + name.upper()

        def envvars_it(v):
            for input, output in values:
                yield v, (str(input), output)
        with Context() as ctx:
            opts = section(ctx)
            self.assertEqual(get_fn(opts), getattr(opts, default_name))
        with Context() as ctx:
            opts = section(ctx)
            if type_error is not None:
                self.assertRaises(TypeError, set_fn, opts, type_error)
            if value_error is not None:
                self.assertRaises(ValueError, setattr, set_fn, value_error)
            for t in values:
                input, output = t
                set_fn(opts, input)
                self.assertEqual(get_fn(opts), output, t)
        with Context() as ctx:
            cleanup: dict[str, Union[str, None]] = {}
            it = itertools.chain(*map(envvars_it, envvars))
            for t in reversed(list(it)):
                var, (input, output) = t
                if var in os.environ:
                    cleanup[var] = os.environ[var]
                else:
                    cleanup[var] = None
                os.environ[var] = input
                opts = type(section(ctx))()
                self.assertEqual(get_fn(opts), output, t)
            for var, val in cleanup.items():
                if val is not None:
                    os.environ[var] = val
                else:
                    del os.environ[var]

    def test_base_filter(self) -> None:
        self._test_option(
            section=lambda ctx: ctx.options.store,
            name='base_filter',
            values=[
                (Filter(Item('x')), Filter(Item('x'))),
                (Filter(None, Property('y')), Filter(None, Property('y')))],
            type_error=0)

    def test_best_ranked(self) -> None:
        self._test_option_bool(
            section=lambda ctx: ctx.options.store,
            name='best_ranked',
            envvars=['KIF_STORE_BEST_RANKED'])

    def test_debug(self) -> None:
        self._test_option_bool(
            section=lambda ctx: ctx.options.store,
            name='debug',
            envvars=['KIF_STORE_DEBUG'])

    def test_distinct(self) -> None:
        self._test_option_bool(
            section=lambda ctx: ctx.options.store,
            name='distinct',
            envvars=['KIF_STORE_DISTINCT'])

    def test_extra_references(self) -> None:
        self._test_option(
            section=lambda ctx: ctx.options.store,
            name='extra_references',
            values=[
                ([[Property('x')(Item('y'))]],
                 ReferenceRecordSet(ReferenceRecord(
                     Property('x')(Item('y')))))],
            type_error=0)

    def test_max_limit(self) -> None:
        self._test_option_int(
            section=lambda ctx: ctx.options.store,
            name='max_limit',
            envvars=['KIF_STORE_MAX_LIMIT'],
            lower_bound=0)

    def test_limit(self) -> None:
        self._test_option_int(
            section=lambda ctx: ctx.options.store,
            name='limit',
            envvars=['KIF_STORE_LIMIT'],
            lower_bound=0,
            optional=True)

    def test_lookahead(self) -> None:
        self._test_option_int(
            section=lambda ctx: ctx.options.store,
            name='lookahead',
            envvars=['KIF_STORE_LOOKAHEAD'],
            lower_bound=1)

    def test_max_page_size(self) -> None:
        self._test_option_int(
            section=lambda ctx: ctx.options.store,
            name='max_page_size',
            envvars=['KIF_STORE_MAX_PAGE_SIZE'],
            lower_bound=0)

    def test_page_size(self) -> None:
        self._test_option_int(
            section=lambda ctx: ctx.options.store,
            name='page_size',
            envvars=['KIF_STORE_PAGE_SIZE'],
            lower_bound=0)

    def test_max_timeout(self) -> None:
        self._test_option_float(
            section=lambda ctx: ctx.options.store,
            name='max_timeout',
            envvars=['KIF_STORE_MAX_TIMEOUT'],
            lower_bound=0.)

    def test_timeout(self) -> None:
        self._test_option_float(
            section=lambda ctx: ctx.options.store,
            name='timeout',
            envvars=['KIF_STORE_TIMEOUT'],
            lower_bound=0.,
            optional=True)


if __name__ == '__main__':
    Test.main()

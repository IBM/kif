# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Item, Property, ReferenceRecord, ReferenceRecordSet

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

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

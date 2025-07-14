# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import Filter, Item, Property, ReferenceRecord, ReferenceRecordSet
from kif_lib.context import Context, Section
from kif_lib.typing import Sequence

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.store

    def test_base_filter(self) -> None:
        self._test_option(
            section=self.section,
            name='base_filter',
            values=[
                (Filter(Item('x')), Filter(Item('x'))),
                (Filter(None, Property('y')), Filter(None, Property('y')))],
            type_error=0)

    def test_debug(self) -> None:
        self._test_debug()

    def _test_debug(
            self,
            envvars: Sequence[str] = ('KIF_STORE_DEBUG',)
    ) -> None:
        self._test_option_bool(
            section=self.section,
            name='debug',
            envvars=envvars)

    def test_distinct(self) -> None:
        self._test_distinct()

    def _test_distinct(
            self,
            envvars: Sequence[str] = ('KIF_STORE_DISTINCT',)
    ) -> None:
        self._test_option_bool(
            section=self.section,
            name='distinct',
            envvars=envvars)

    def test_max_distinct_window_size(self) -> None:
        self._test_max_distinct_window_size()

    def _test_max_distinct_window_size(
            self,
            envvars: Sequence[str] = ('KIF_STORE_MAX_DISTINCT_WINDOW_SIZE',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='max_distinct_window_size',
            envvars=envvars,
            lower_bound=1)

    def test_distinct_window_size(self) -> None:
        self._test_distinct_window_size()

    def _test_distinct_window_size(
            self,
            envvars: Sequence[str] = ('KIF_STORE_DISTINCT_WINDOW_SIZE',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='distinct_window_size',
            envvars=envvars,
            lower_bound=1)

    def test_extra_references(self) -> None:
        self._test_option(
            section=self.section,
            name='extra_references',
            values=[
                ([[Property('x')(Item('y'))]],
                 ReferenceRecordSet(ReferenceRecord(
                     Property('x')(Item('y')))))],
            type_error=0)

    def test_max_limit(self) -> None:
        self._test_max_limit()

    def _test_max_limit(
            self,
            envvars: Sequence[str] = ('KIF_STORE_MAX_LIMIT',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='max_limit',
            envvars=envvars,
            lower_bound=0)

    def test_limit(self) -> None:
        self._test_limit()

    def _test_limit(
            self,
            envvars: Sequence[str] = ('KIF_STORE_LIMIT',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='limit',
            envvars=envvars,
            lower_bound=0,
            optional=True)

    def test_lookahead(self) -> None:
        self._test_lookahead()

    def _test_lookahead(
            self,
            envvars: Sequence[str] = ('KIF_STORE_LOOKAHEAD',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='lookahead',
            envvars=envvars,
            lower_bound=1)

    def test_omega(self) -> None:
        self._test_omega()

    def _test_omega(
            self,
            envvars: Sequence[str] = ('KIF_STORE_OMEGA',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='omega',
            envvars=envvars,
            lower_bound=1)

    def test_max_page_size(self) -> None:
        self._test_max_page_size()

    def _test_max_page_size(
            self,
            envvars: Sequence[str] = ('KIF_STORE_MAX_PAGE_SIZE',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='max_page_size',
            envvars=envvars,
            lower_bound=0)

    def test_page_size(self) -> None:
        self._test_page_size()

    def _test_page_size(
            self,
            envvars: Sequence[str] = ('KIF_STORE_PAGE_SIZE',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='page_size',
            envvars=envvars,
            lower_bound=0)

    def test_max_timeout(self) -> None:
        self._test_max_timeout()

    def _test_max_timeout(
            self,
            envvars: Sequence[str] = ('KIF_STORE_MAX_TIMEOUT',)
    ) -> None:
        self._test_option_float(
            section=self.section,
            name='max_timeout',
            envvars=envvars,
            lower_bound=0.)

    def test_timeout(self) -> None:
        self._test_timeout()

    def _test_timeout(
            self,
            envvars: Sequence[str] = ('KIF_STORE_TIMEOUT',)
    ) -> None:
        self._test_option_float(
            section=self.section,
            name='timeout',
            envvars=envvars,
            lower_bound=0.,
            optional=True)


if __name__ == '__main__':
    Test.main()

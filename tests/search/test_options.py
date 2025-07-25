# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import Sequence

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.search

    def test_debug(self) -> None:
        self._test_debug()

    def _test_debug(
            self,
            envvars: Sequence[str] = ('KIF_SEARCH_DEBUG',)
    ) -> None:
        self._test_option_bool(
            section=self.section,
            name='debug',
            envvars=envvars)

    def test_language(self) -> None:
        self._test_language()

    def _test_language(
            self,
            envvars: Sequence[str] = ('KIF_SEARCH_LANGUAGE',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='language',
            envvars=envvars,
            optional=True)

    def test_max_limit(self) -> None:
        self._test_max_limit()

    def _test_max_limit(
            self,
            envvars: Sequence[str] = ('KIF_SEARCH_MAX_LIMIT',)
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
            envvars: Sequence[str] = ('KIF_SEARCH_LIMIT',)
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
            envvars: Sequence[str] = ('KIF_SEARCH_LOOKAHEAD',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='lookahead',
            envvars=envvars,
            lower_bound=1)

    def test_max_page_size(self) -> None:
        self._test_max_page_size()

    def _test_max_page_size(
            self,
            envvars: Sequence[str] = ('KIF_SEARCH_MAX_PAGE_SIZE',)
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
            envvars: Sequence[str] = ('KIF_SEARCH_PAGE_SIZE',)
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
            envvars: Sequence[str] = ('KIF_SEARCH_MAX_TIMEOUT',)
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
            envvars: Sequence[str] = ('KIF_SEARCH_TIMEOUT',)
    ) -> None:
        self._test_option_float(
            section=self.section,
            name='timeout',
            envvars=envvars,
            lower_bound=0.,
            optional=True)


if __name__ == '__main__':
    Test.main()

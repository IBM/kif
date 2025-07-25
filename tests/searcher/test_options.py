# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import Sequence

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.searcher

    def test_debug(self) -> None:
        self._test_debug()

    def _test_debug(
            self,
            envvars: Sequence[str] = ('KIF_SEARCHER_DEBUG',)
    ) -> None:
        self._test_option_bool(
            section=self.section,
            name='debug',
            envvars=envvars)

    def test_max_limit(self) -> None:
        self._test_max_limit()

    def _test_max_limit(
            self,
            envvars: Sequence[str] = ('KIF_SEARCHER_MAX_LIMIT',)
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
            envvars: Sequence[str] = ('KIF_SEARCHER_LIMIT',)
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
            envvars: Sequence[str] = ('KIF_SEARCHER_LOOKAHEAD',)
    ) -> None:
        self._test_option_int(
            section=self.section,
            name='lookahead',
            envvars=envvars,
            lower_bound=1)


if __name__ == '__main__':
    Test.main()

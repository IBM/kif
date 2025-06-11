# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import override

from ..test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.store.sparql

    @override
    def test_best_ranked(self) -> None:
        self._test_best_ranked(['KIF_SPARQL_STORE_BEST_RANKED'])

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_SPARQL_STORE_DEBUG'])

    @override
    def test_distinct(self) -> None:
        self._test_distinct(['KIF_SPARQL_STORE_DISTINCT'])

    @override
    def test_max_distinct_window_size(self) -> None:
        self._test_max_distinct_window_size(
            ['KIF_SPARQL_STORE_MAX_DISTINCT_WINDOW_SIZE'])

    @override
    def test_distinct_window_size(self) -> None:
        self._test_distinct_window_size(
            ['KIF_SPARQL_STORE_DISTINCT_WINDOW_SIZE'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_SPARQL_STORE_MAX_LIMIT'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_SPARQL_STORE_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_SPARQL_STORE_LOOKAHEAD'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_SPARQL_STORE_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_SPARQL_STORE_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_SPARQL_STORE_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_SPARQL_STORE_TIMEOUT'])

    def test_skolemize(self) -> None:
        self._test_option_bool(
            section=self.section,
            name='skolemize',
            envvars=['KIF_SPARQL_STORE_SKOLEMIZE'])


if __name__ == '__main__':
    Test.main()

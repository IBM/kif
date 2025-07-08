# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import override

from ..test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.store.empty

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_EMPTY_STORE_DEBUG'])

    @override
    def test_distinct(self) -> None:
        self._test_distinct(['KIF_EMPTY_STORE_DISTINCT'])

    @override
    def test_max_distinct_window_size(self) -> None:
        self._test_max_distinct_window_size(
            ['KIF_EMPTY_STORE_MAX_DISTINCT_WINDOW_SIZE'])

    @override
    def test_distinct_window_size(self) -> None:
        self._test_distinct_window_size(
            ['KIF_EMPTY_STORE_DISTINCT_WINDOW_SIZE'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_EMPTY_STORE_MAX_LIMIT'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_EMPTY_STORE_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_EMPTY_STORE_LOOKAHEAD'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_EMPTY_STORE_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_EMPTY_STORE_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_EMPTY_STORE_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_EMPTY_STORE_TIMEOUT'])


if __name__ == '__main__':
    Test.main()

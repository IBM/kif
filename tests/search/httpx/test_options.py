# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import override, Sequence

from ..test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.search.httpx

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_HTTPX_SEARCH_DEBUG'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_HTTPX_SEARCH_MAX_LIMIT'])

    @override
    def test_language(self) -> None:
        self._test_language(['KIF_HTTPX_SEARCH_LANGUAGE'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_HTTPX_SEARCH_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_HTTPX_SEARCH_LOOKAHEAD'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_HTTPX_SEARCH_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_HTTPX_SEARCH_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_HTTPX_SEARCH_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_HTTPX_SEARCH_TIMEOUT'])

    # -- httpx --

    def test_iri(self) -> None:
        self._test_iri()

    def _test_iri(
            self,
            envvars: Sequence[str] = ('KIF_HTTPX_SEARCH_IRI',)
    ) -> None:
        self._test_option_iri(
            section=self.section,
            name='iri',
            envvars=envvars)

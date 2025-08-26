# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import override, Sequence

from ..ddgs.test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.search.dbpedia_ddgs

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_DBPEDIA_DDGS_SEARCH_DEBUG'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_DBPEDIA_DDGS_SEARCH_MAX_LIMIT'])

    @override
    def test_language(self) -> None:
        self._test_language(['KIF_DBPEDIA_DDGS_SEARCH_LANGUAGE'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_DBPEDIA_DDGS_SEARCH_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_DBPEDIA_DDGS_SEARCH_LOOKAHEAD'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_DBPEDIA_DDGS_SEARCH_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_DBPEDIA_DDGS_SEARCH_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_DBPEDIA_DDGS_SEARCH_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_DBPEDIA_DDGS_SEARCH_TIMEOUT'])

    # -- ddgs --

    @override
    def test_backend(self) -> None:
        self._test_backend(['KIF_DBPEDIA_DDGS_SEARCH_BACKEND'])

    def test_in_url(self) -> None:
        self._test_in_url(['KIF_DBPEDIA_DDGS_SEARCH_IN_URL'])

    def test_item_match(self) -> None:
        self._test_item_match(['KIF_DBPEDIA_DDGS_SEARCH_ITEM_MATCH'])

    def test_item_sub(self) -> None:
        self._test_item_sub(['KIF_DBPEDIA_DDGS_SEARCH_ITEM_SUB'])

    def test_lexeme_match(self) -> None:
        self._test_lexeme_match(['KIF_DBPEDIA_DDGS_SEARCH_LEXEME_MATCH'])

    def test_lexeme_sub(self) -> None:
        self._test_lexeme_sub(['KIF_DBPEDIA_DDGS_SEARCH_LEXEME_SUB'])

    def test_property_match(self) -> None:
        self._test_property_match(['KIF_DBPEDIA_DDGS_SEARCH_PROPERTY_MATCH'])

    def test_property_sub(self) -> None:
        self._test_property_sub(['KIF_DBPEDIA_DDGS_SEARCH_PROPERTY_SUB'])

    def test_site(self) -> None:
        self._test_site(['KIF_DBPEDIA_DDGS_SEARCH_SITE'])

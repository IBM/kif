# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section
from kif_lib.typing import override, Sequence

from ..test_options import Test as _Test


class Test(_Test):

    @override
    def section(self, ctx: Context) -> Section:
        return ctx.options.search.ddgs

    @override
    def test_debug(self) -> None:
        self._test_debug(['KIF_DDGS_SEARCH_DEBUG'])

    @override
    def test_max_limit(self) -> None:
        self._test_max_limit(['KIF_DDGS_SEARCH_MAX_LIMIT'])

    @override
    def test_language(self) -> None:
        self._test_language(['KIF_DDGS_SEARCH_LANGUAGE'])

    @override
    def test_limit(self) -> None:
        self._test_limit(['KIF_DDGS_SEARCH_LIMIT'])

    @override
    def test_lookahead(self) -> None:
        self._test_lookahead(['KIF_DDGS_SEARCH_LOOKAHEAD'])

    @override
    def test_max_page_size(self) -> None:
        self._test_max_page_size(['KIF_DDGS_SEARCH_MAX_PAGE_SIZE'])

    @override
    def test_page_size(self) -> None:
        self._test_page_size(['KIF_DDGS_SEARCH_PAGE_SIZE'])

    @override
    def test_max_timeout(self) -> None:
        self._test_max_timeout(['KIF_DDGS_SEARCH_MAX_TIMEOUT'])

    @override
    def test_timeout(self) -> None:
        self._test_timeout(['KIF_DDGS_SEARCH_TIMEOUT'])

    # -- ddgs --

    def test_backend(self) -> None:
        self._test_backend()

    def _test_backend(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_BACKEND',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='backend',
            envvars=envvars)

    def test_in_url(self) -> None:
        self._test_in_url()

    def _test_in_url(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_IN_URL',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='in_url',
            envvars=envvars)

    def test_item_match(self) -> None:
        self._test_item_match()

    def _test_item_match(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_ITEM_MATCH',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='item_match',
            envvars=envvars)

    def test_item_sub(self) -> None:
        self._test_item_sub()

    def _test_item_sub(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_ITEM_SUB',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='item_sub',
            envvars=envvars)

    def test_lexeme_match(self) -> None:
        self._test_lexeme_match()

    def _test_lexeme_match(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_LEXEME_MATCH',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='lexeme_match',
            envvars=envvars)

    def test_lexeme_sub(self) -> None:
        self._test_lexeme_sub()

    def _test_lexeme_sub(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_LEXEME_SUB',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='lexeme_sub',
            envvars=envvars)

    def test_property_match(self) -> None:
        self._test_property_match()

    def _test_property_match(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_PROPERTY_MATCH',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='property_match',
            envvars=envvars)

    def test_property_sub(self) -> None:
        self._test_property_sub()

    def _test_property_sub(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_PROPERTY_SUB',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='property_sub',
            envvars=envvars)

    def test_site(self) -> None:
        self._test_site()

    def _test_site(
            self,
            envvars: Sequence[str] = ('KIF_DDGS_SEARCH_SITE',)
    ) -> None:
        self._test_option_str(
            section=self.section,
            name='site',
            envvars=envvars)

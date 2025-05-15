# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib.context import Context, Section

from ..tests import OptionsTestCase


class Test(OptionsTestCase):

    def section(self, ctx: Context) -> Section:
        return ctx.options.vocabulary.wd

    def test_resolver(self) -> None:
        self._test_option_iri(
            section=self.section,
            name='resolver',
            envvars=['KIF_VOCABULARY_WD_RESOLVER', 'WIKIDATA'],
            optional=True)

    def test_item_cache(self) -> None:
        self._test_option_path(
            section=self.section,
            name='item_cache',
            envvars=['KIF_VOCABULARY_WD_ITEM_CACHE'],
            optional=True)

    def test_property_cache(self) -> None:
        self._test_option_path(
            section=self.section,
            name='property_cache',
            envvars=['KIF_VOCABULARY_WD_PROPERTY_CACHE'],
            optional=True)

if __name__ == '__main__':
    Test.main()
